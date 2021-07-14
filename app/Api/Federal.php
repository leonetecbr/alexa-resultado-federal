<?php

namespace Leone\Results\Api;

/**
 * Pega o resultado da Federal de um site
 */
class Federal{
  
  /*
   * Pega os dados da URL da API
   * @param string $url
   * @return array
   */
  private static function getApi($url){
    $c = curl_init();
    $cookie_file = __DIR__.'/federal.txt';
    $options = array(
      CURLOPT_URL => $url,
      CURLOPT_REFERER => 'http://www.loterias.caixa.gov.br',
      CURLOPT_USERAGENT => 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_CONNECTTIMEOUT => 6,
      CURLOPT_TIMEOUT => 6,
      CURLOPT_MAXREDIRS => 1,
      CURLOPT_FOLLOWLOCATION => true,
      CURLOPT_COOKIESESSION => true,
      CURLOPT_COOKIEFILE => $cookie_file,
      CURLOPT_COOKIEJAR => $cookie_file
    );
    curl_setopt_array($c, $options);
    $json = curl_exec($c);
    curl_close($c);
    $array = json_decode($json , true);
    if (!empty($array)) {
      $dados['resultados'] = $array['dezenasSorteadasOrdemSorteio'];
      $dados['number'] = $array['numero'];
      $dados['data'] = $array['dataApuracao'];
      $dados['url'] = $url;
    }else{
      return 'Estamos com problemas para obter o resultado';
    }
    return $dados;
  }
  
  /**
   * Pega a URL para consulta dos dados
   * @param integer $conc
   * @return string
   */
  private static function getUrl($conc = ''){
    if (!empty($conc)) {
      $conc = '&concurso='.$conc;
    }
    $c = curl_init();
    $cookie_file = __DIR__.'/federal.txt';
    $options = array(
      CURLOPT_URL => 'http://www.loterias.caixa.gov.br/wps/portal/loterias/landing/federal',
      CURLOPT_REFERER => 'http://www.loterias.caixa.gov.br',
      CURLOPT_USERAGENT => 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_CONNECTTIMEOUT => 6,
      CURLOPT_TIMEOUT => 6,
      CURLOPT_MAXREDIRS => 1,
      CURLOPT_FOLLOWLOCATION => true,
      CURLOPT_COOKIESESSION => true,
      CURLOPT_COOKIEFILE => $cookie_file,
      CURLOPT_COOKIEJAR => $cookie_file
    );
    curl_setopt_array($c, $options);
      
    try {
      $content = curl_exec($c);
      $data = curl_getinfo($c);
      $errno = curl_errno($c);
      $errmsg = curl_error($c);
      if ((int)$errno !== 0 || (int)$data['http_code'] !== 200) {
      return 'Estamos com problemas para obter o resultado';
      }
    } catch (HttpException $ex) {
      return 'Estamos com problemas para obter o resultado';
    }
    curl_close($c);
    $p1 = '/\<link id="com\.ibm\.lotus\.NavStateUrl" rel="alternate" href="(.*)" \/\>/';
    $p2 = '/\<input type="hidden" value="(.*)" ng\-model="urlBuscarResultado" id="urlBuscarResultado" \/\>/';
    if(!preg_match($p1, $content, $r1) || !preg_match($p2, $content, $r2)){
      return 'Estamos com problemas para obter o resultado';
    }
    return 'http://www.loterias.caixa.gov.br'.$r1[1].$r2[1].'?timestampAjax='.str_replace('.', '', microtime(true)).$conc;
  }
  
  /**
   * Pega os resultado do site ou do cache
   * @param integer $conc
   * @return array
   */
  private static function get($conc = ''){
    $cached = false;
    $file = __DIR__.'/../../resources/cache/federal'.$conc.'.json';
    $pfile = __DIR__.'/../../resources/cache/federal.json';
    if (empty($conc)) {
      if (file_exists($file)) {
        if (intval(date("Hm"))>=1930){
        if ((time()-fileatime($file))<$_ENV['CACHE_TIME_SHORT']) {
          $cached = true;
        }
        }elseif ((time()-fileatime($file))<$_ENV['CACHE_TIME_LONG']) {
        $cached = true;
        }
      }
    }elseif (file_exists($file)) {
      $cached = true;
    }
    
    if (!$cached) {
      if (file_exists($file)) {
        $dado = json_decode(file_get_contents($file), true);
        $url = $dado['url'];
        $dados = self::getApi($url);
      }elseif (!empty($conc) && file_exists($pfile)){
        $dado = json_decode(file_get_contents($pfile), true);
        $url = $dado['url'].'&concurso='.$conc;
        $dados = self::getApi($url);
      }
      if (!is_array($dados)) {
        $url = self::getUrl($conc);
        $dados = self::getApi($url);
      }
      file_put_contents($file, json_encode($dados));
      return $dados;
    }else{
      return json_decode(file_get_contents($file), true);
    }
  }
  
  /**
   * Transforma o resultado em texto para ser lido pela alexa
   * @param array $dados
   * @param integer $conc
   * @return string
   */
  public static function getText($dados = null, $conc = ''){
    if (empty($dados)) {
      $dados = self::get($conc);
    }
    for ($i=0;$i<5; $i++) {
      $dados['resultados'][$i] = rtrim(chunk_split(substr($dados['resultados'][$i], 2), 2, ' '));
    }
    return 'O resultado da Loteria Federal pelo concurso '.$dados['number'].' no dia '.$dados['data'].' foi: 1º Prêmio: '.$dados['resultados'][0].', 2º Prêmio: '.$dados['resultados'][1].', 3º Prêmio: '.$dados['resultados'][2].', 4º Prêmio: '.$dados['resultados'][3].', 5º Prêmio: '.$dados['resultados'][4].'.';
  }
  
  /**
   * Transforma o resultado em card para ser mostrado pela alexa
   * @param array $dados
   * @param integer $conc
   * @return string
   */
  public static function getCard($dados = null, $conc = ''){
    if (empty($dados)) {
      $dados = self::get($conc);
    }
    return "Concurso: {$dados['number']}\nData: {$dados['data']}\n1º Prêmio: {$dados['resultados'][0]}\n2º Prêmio: {$dados['resultados'][1]}\n3º Prêmio: {$dados['resultados'][2]}\n4º Prêmio: {$dados['resultados'][3]}\n5º Prêmio: {$dados['resultados'][4]}";
  }

  /**
   * Pega o resultado por número do concurso
   * @param integer $number
   * @return array
   */
  public static function getNumber($number){
    $dados = self::get();
    if ($number>$dados['number']) {
      $text = 'O concurso '.$number.' ainda não foi sorteado.';
      return ['card' => $text, 'text' => $text];
    }elseif ($number==$dados['number']) {
      return ['card' => self::getCard($dados, $number), 'text' => self::getText($dados, $number)];
    }else{
      return ['card' => self::getCard('', $number), 'text' => self::getText('', $number)];
    }
  }
}