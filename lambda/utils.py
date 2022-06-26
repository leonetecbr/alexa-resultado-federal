import requests


class Federal:
    """Pega o resultado da Loteria Federal da API da Caixa Econômica Federal"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120'
                          ' Mobile Safari/537.36',
            'Referer': 'http://www.loterias.caixa.gov.br'
        }
        self.cookies = {
            'security': 'true'
        }
        self.concourse = 0

    def getApi(self):
        """
        Obtém o resultado da Loteria Federal através da API da Caixa Econômica Federal
        :return dict
        """
        url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/federal/'
        if self.concourse >= 1:
            url += str(self.concourse)

        response = requests.get(url, headers=self.headers, cookies=self.cookies, verify=False)

        resultado = response.json()

        return resultado

    def get(self, concourse=0):
        """
        Obtém o resultado da Loteria Federal para o concurso pedido, 0 retorna o último resultado
        :param concourse: int
        :return dict
        """
        self.concourse = concourse
        data = self.getApi()

        return data


def getText(result):
    """
    Gera o texto para ser falado com o resultado
    :param result: dict
    :return string
    """
    concourse = str(result['numero'])
    if len(str(concourse)) == 4:
        concourse = concourse[:2] + ' ' + concourse[2:]
    return f'O resultado da Loteria Federal pelo concurso {concourse}, no dia {result["dataApuracao"]} foi: ' \
           f'1º Prêmio: {result["listaDezenas"][0][2:4]} ' + \
           result['listaDezenas'][0][4:] + ', 2º Prêmio: ' + result['listaDezenas'][1][2:4] + ' ' + \
           result['listaDezenas'][1][4:] + ', 3º Prêmio: ' + result['listaDezenas'][2][2:4] + ' ' + \
           result['listaDezenas'][2][4:] + ', 4º Prêmio: ' + result['listaDezenas'][3][2:4] + ' ' + \
           result['listaDezenas'][3][4:] + ', 5º Prêmio: ' + result['listaDezenas'][4][2:4] + ' ' + \
           result['listaDezenas'][4][4:] + '. Este resultado foi fornecido pela Caixa Econômica Federal.'


def getDozens(result):
    """
    Gera o texto das dezenas para ser falado com o resultado
    :param result: dict
    :return string
    """
    concourse = str(result['numero'])
    return f'O resultado da Loteria Federal pelo concurso {concourse}, no dia ' + result['dataApuracao'] + ' foi: ' \
            '1º Prêmio: ' + result['listaDezenas'][0][4:] + ', 2º Prêmio: ' + result['listaDezenas'][1][4:] + \
            ', 3º Prêmio: ' + result['listaDezenas'][2][4:] + ', 4º Prêmio: ' + result['listaDezenas'][3][4:] + \
            ', 5º Prêmio: ' + result['listaDezenas'][4][4:] + '. Este resultado foi fornecido pela Caixa Econômica ' \
                                                             'Federal.'


def getCard(result):
    """
    Gera a estrutura do card com o resultado
    :param result: dict
    :return string
    """
    return 'Concurso: ' + str(result['numero']) + '\nData: ' + result['dataApuracao'] + '\n1º Prêmio: ' + \
           result['listaDezenas'][0] + '\n2º Prêmio: ' + result['listaDezenas'][1] + '\n3º Prêmio: ' + \
           result['listaDezenas'][2] + '\n4º Prêmio: ' + result['listaDezenas'][3] + '\n5º Prêmio: ' + \
           result['listaDezenas'][4] + '\nFonte: Caixa Econômica Federal'
