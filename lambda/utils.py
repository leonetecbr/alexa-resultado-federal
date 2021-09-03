import logging
import os
import boto3
from botocore.exceptions import ClientError
import requests, re, time
from datetime import datetime

def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object with a capped expiration of 60 seconds

    :param object_name: string
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3',
                             region_name=os.environ.get('S3_PERSISTENCE_REGION'),
                             config=boto3.session.Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    try:
        bucket_name = os.environ.get('S3_PERSISTENCE_BUCKET')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=60*1)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


class Federal():
    """Pega o resultado da federal do cache ou da api da Caixa Econômica Federal"""
    
    def __init__(self):
        self.h = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Referer': 'http://www.loterias.caixa.gov.br'
        }
        self.c = {
            'security': 'true'
        }
        self.conc = 0

    def generateUrl(self):
        response = requests.get('http://www.loterias.caixa.gov.br/wps/portal/loterias/landing/federal', headers=self.h, cookies=self.c)
        
        txt = response.text
        
        p1 = re.search('\<link id="com\.ibm\.lotus\.NavStateUrl" rel="alternate" href="(.*)" \/\>', txt)
        
        p2 = re.search('\<input type="hidden" value="(.*)" ng\-model="urlBuscarResultado" id="urlBuscarResultado" \/\>', txt)
        
        url = 'http://www.loterias.caixa.gov.br'+p1.group(1)+p2.group(1)+'?timestampAjax='
        
        return url
    
    def getUrl(self):
        url = self.generateUrl()
        url += str(time.time()).replace('.', '')
        return url
    
    def getApi(self):
        url = self.getUrl()
        if self.conc > 1:
            url += '&concurso='+str(self.conc)
        response = requests.get(url, headers=self.h, cookies=self.c)
        resultado = response.json()
        if response == '':
            self.generateUrl()
            self.getApi()
        return resultado
    
    def get(self, conc = 0):
        self.conc = conc
        dados = self.getApi()
        
        return dados

def getText(resultado):
    """Gera o texto para ser falado com o resultado"""
    concurso = str(resultado['numero'])
    return 'O resultado da Loteria Federal pelo concurso '+concurso[:2]+' '+concurso[2:]+', no dia '+resultado['dataApuracao']+' foi: 1º Prêmio: '+resultado['listaDezenas'][0][2:4]+' '+resultado['listaDezenas'][0][4:]+', 2º Prêmio: '+resultado['listaDezenas'][1][2:4]+' '+resultado['listaDezenas'][1][4:]+', 3º Prêmio: '+resultado['listaDezenas'][2][2:4]+' '+resultado['listaDezenas'][2][4:]+', 4º Prêmio: '+resultado['listaDezenas'][3][2:4]+' '+resultado['listaDezenas'][3][4:]+', 5º Prêmio: '+resultado['listaDezenas'][4][2:4]+' '+resultado['listaDezenas'][4][4:]+'. Este resultado foi fornecido pela Caixa Econômica Federal.'

def getCard(resultado):
    """Gera a estrutura do card com o resultado"""
    return 'Concurso: '+str(resultado['numero'])+'\nData: '+resultado['dataApuracao']+'\n1º Prêmio: '+resultado['listaDezenas'][0]+'\n2º Prêmio: '+resultado['listaDezenas'][1]+'\n3º Prêmio: '+resultado['listaDezenas'][2]+'\n4º Prêmio: '+resultado['listaDezenas'][3]+'\n5º Prêmio: '+resultado['listaDezenas'][4]+'\nFonte: Caixa Econômica Federal'
