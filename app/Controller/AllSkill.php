<?php
namespace Leone\Loteria\Federal\Controller;

use \Alexa\Skill_Template;
use \Leone\Loteria\Federal\Api;

class AllSkill extends Skill_Template {
  
  /**
   * Pega o texto para envio do resultado e transforma no JSON  
   */
  private function sendResultFederalLast(){
    $intent_text = Api\Federal::getText();
	  $intent_card = Api\Federal::getCard();
		$this->output()->response()->output_speech()->set_text($intent_text.' Quer que eu repita ?');
		$this->output()->response()->card()->set_title('Resultado da Loteria Federal');
		$this->output()->response()->card()->set_text($intent_card);
  }
  
  /**
   * Pega o texto para envio do resultado e transforma no JSON  
   */
  private function sendResultFederalNumber(){
    $concurso = $this->input()->request()->intent()->get_slot_value('number');
    if (empty($concurso) || $concurso == '?'){
      return $this->failed_request();
    }
    $concurso = intval($concurso);
    if ($concurso<1) {
      return $this->failed_request();
    }
    $intent = Api\Federal::getNumber($concurso);
		$this->output()->response()->output_speech()->set_text($intent['text']);
		$this->output()->response()->card()->set_title('Resultado da Loteria Federal');
		$this->output()->response()->card()->set_text($intent['card']);
		$this->output()->response()->end_session();
  }
  
  /**
   * Gera um número aleatório e tranforma a resposta em JSON
   */
  private function sendRandomFederal(){
    $rand = str_pad(mt_rand(0, 9999), 4, '0' , STR_PAD_LEFT);
    $rand = rtrim(chunk_split($rand, 2, ' '));
    $text = 'Pensei! Mas antes de falar, quero te dizer que ele é apenas um número gerado aleatoriamente, não garanto que ele seja sorteado. Ok? Eu pensei no número '.$rand;
		$this->output()->response()->output_speech()->set_text($text);
		$this->output()->response()->card()->set_title('Palpite Loteria Federal');
		$this->output()->response()->card()->set_text($text);
		
		$this->output()->response()->end_session();
  }
  
  /**
   * Processa o Intent e direciona ao método correspondente
   */
  private function processIntent(){
    switch ($this->input()->request()->intent()->get_name()) {
      case 'AMAZON.StopIntent':
        $this->end_request();
        break;
      
      case 'AMAZON.CancelIntent':
        $this->end_request();
        break;
      
      case 'LastFederalIntent':
        $this->sendResultFederalLast();
        break;
      
      case 'NumberFederalIntent':
        $this->sendResultFederalNumber();
        break;
      
      case 'RandomFederalIntent':
        $this->sendRandomFederal();
        break;
      
      case 'AMAZON.HelpIntent':
        $this->help_request();
        break;
      
      default:
        $this->failed_request();
    }
  }
  
  /**
   * Um Intent foi recebibo
   */
	public function intent_request() {
	  $this->processIntent();
	}
	
	/**
   * A Skill foi iniciada
   */
	public function launch_request() {
	  $intent_text = 'Olá, o que você quer saber ? Diga último resultado, resultado do concurso 5000 ou peça um palpite.';
  	$this->output()->response()->output_speech()->set_text($intent_text);
		$this->output()->response()->card()->set_title('O que deseja saber ?');
		$this->output()->response()->card()->set_text($intent_text);
	}
	
	/**
   * Intent não locaizado
   */
	public function failed_request(){
	  $this->output()->response()->output_speech()->set_text('Não entendi o que você disse, tente novamente de outra forma.');
		$this->output()->response()->card()->set_title('Não entendi!');
		$this->output()->response()->card()->set_text('Não entendi o que você disse, tente novamente de outra forma.');
	}
	
	/**
   * O usuário pediu ajuda
   */
	public function help_request() {
	  $intent_card = "• \"Último resultado\" para ouvir o último resultado disponível. \n• Resultado do concurso + o número do concurso que você quer. Ex: \"Resultado do concurso 5000\", para ouvir o resultado do concurso 5000. \n• \"Me dê um palpite\" para ouvir um número gerado aleatoriamente.";
	   $intent_text = 'Você pode dizer "último resultado" para ouvir o último resultado disponível, resultado do concurso mais o número do concurso que você quer, por exemplo, "resultado do concurso 5000" para ouvir o resultado do concurso 5000, "me dê um palpite" para ouvir um número gerado aleatoriamente.';
  	$this->output()->response()->output_speech()->set_text($intent_text);
		$this->output()->response()->card()->set_title('Você pode dizer:');
		$this->output()->response()->card()->set_text($intent_card);
	}
	/**
   * A Skill foi encerrada
   */
	public function end_request() {
  	$this->output()->response()->output_speech()->set_text('Tchau, espero você na próxima.');
		$this->output()->response()->card()->set_title('Tchau!');
		$this->output()->response()->card()->set_text('Tchau, espero você na próxima.');

		$this->output()->response()->end_session();
	}
}