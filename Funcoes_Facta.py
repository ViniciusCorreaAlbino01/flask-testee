import requests,json
import http.client


def get_token_facta():
        url = 'https://webservice.facta.com.br/gera-token'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',"Authorization":"Basic OTI3NDM6YjByemEyeXNvZnc2Z212azF6aWs="}
        

        response = requests.get(url,headers=headers).json()
        token = response['token']
        return token


def simular_facta(token,valor_parcela,prazo,cpf,data_nascimento,especie):
     cpf = cpf[0:3] + '.' + cpf[3:6] + '.' + cpf[6:9]+ '-' + cpf[9:]    
     url = f'https://webservice.facta.com.br/proposta/operacoes-disponiveis?produto=D&tipo_operacao=13&averbador=3&convenio=3&opcao_valor=2&valor_parcela={valor_parcela}&prazo={prazo}&cpf={cpf}&data_nascimento={data_nascimento}'
     headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',"Authorization":f'Bearer {token}'
     }

     response = requests.get(url,headers=headers).json()
     if response['erro'] == False:
          for tabelas in response['tabelas']:
               codigo_tabela = tabelas['codigoTabela']
               if especie == '87' and codigo_tabela == 99587:
                    tabela = tabelas
               if especie == '88' and codigo_tabela == 101862:
                    tabela = tabelas
               if especie != '88' and especie != '87' and codigo_tabela == 102636:
                    tabela = tabelas
          codigo_tabela = tabela['codigoTabela']
          valor_operacao = tabela['contrato']
          coeficiente = tabela['coeficiente']
          taxa = tabela['taxa']


          return taxa,codigo_tabela,valor_operacao,coeficiente
     else:
          return 'erro','erro','erro', 'erro'

    

def cadastrar_simulacao_facta(token,tipo_operacao,cpf,data_nascimento,codigo_tabela,prazo,valor_operacao,valor_parcela,coeficiente):
     data_nascimento = data_nascimento[8:] + '/' +  data_nascimento[5:7] + '/'+ data_nascimento[:4]

     url = 'https://webservice.facta.com.br/proposta/etapa1-simulador'
     headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',"Authorization":f'Bearer {token}'
     }
     payload = {
          "produto":"D","tipo_operacao":tipo_operacao,"averbador":"3","convenio":"3","cpf":cpf,"data_nascimento":data_nascimento,"login_certificado":"92743","codigo_tabela":codigo_tabela,"prazo":prazo,'valor_operacao':valor_operacao,"valor_parcela":valor_parcela,"coeficiente":coeficiente
     }

     response = requests.post(url,data=payload,headers=headers).json()
     id_simulador = response['id_simulador']
     return id_simulador

def cadastrar_dados_pessoais_facta(token,id_simulador,cpf,nome,sexo,estado_civil,data_nascimento,rg,estado_rg,orgao_emissor,data_expedicao,estado_natural,cidade_natural,celular,renda,cep,endereco,numero,bairro,cidade,estado,nome_mae,nome_pai,banco,agencia,conta,matricula,tipo_credito_nb,especie,banco_pagamento,agencia_pagamento,conta_pagamento):
     celular = '(0' + celular[0:2] + ')' + celular[2:7] + '-' + celular[7:]
     cpf = cpf[0:3] + '.' + cpf[3:6] + '.' + cpf[6:9]+ '-' + cpf[9:]
     url = 'https://webservice.facta.com.br/proposta/etapa2-dados-pessoais'
     headers = {
         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',"Authorization":f'Bearer {token}'
    }
     payload = {
         "id_simulador":id_simulador,"cpf":cpf,"nome":nome,'sexo':sexo,'estado_civil':estado_civil,'data_nascimento':data_nascimento,'rg':rg,'estado_rg':estado_rg,'orgao_emissor':orgao_emissor,'data_expedicao':data_expedicao,'estado_natural':estado_natural,'cidade_natural':cidade_natural,'nacionalidade':'1','celular':celular,'renda':renda,'cep':cep,'endereco':endereco,'numero':numero,'bairro':bairro,'cidade':cidade,'estado':estado,'nome_mae':nome_mae,'nome_pai':nome_pai,'valor_patrimonio':'1','cliente_iletrado_impossibilitado':"N",'banco':banco,'agencia':agencia,'conta':conta,'matricula':matricula,'tipo_credito_nb':tipo_credito_nb,'tipo_beneficio':especie,'estado_beneficio':estado,'banco_pagamento':banco_pagamento,'agencia_pagamento':agencia_pagamento,'conta_pagamento':conta_pagamento
    }

     response = requests.post(url,data=payload,headers=headers).json()
     print(response)
     if response['erro']:
          try:
               return response['mensagem']
          except:
               return response['message']
     else:
          codigo_cliente = response['codigo_cliente']
          return codigo_cliente


def finalizar_cadastro_facta(token,codigo_cliente,id_simulador):
     url = 'https://webservice.facta.com.br/proposta/etapa3-proposta-cadastro'

     headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',"Authorization":f'Bearer {token}'
     }
          
     payload = {
               'codigo_cliente':codigo_cliente,'id_simulador':id_simulador
          }

     response = requests.post(url,data=payload,headers=headers).json()
     af = response['codigo']
     url = response['url_formalizacao']
     return af,url

     
def url_facta(token,af):
     url = 'https://webservice.facta.com.br/proposta/envio-link'
     headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',"Authorization":f'Bearer {token}'
     }
     payload = {
          'codigo_af':af,'tipo_envio':'whatsapp'
     }

     response = requests.post(url,data=payload,headers=headers)


def get_cidade_facta(token,estado,cidade):
     url = f"https://webservice.facta.com.br/proposta-combos/cidade?estado={estado}&nome_cidade={cidade}"
     headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',"Authorization":f'Bearer {token}'
}

     try:
          response = requests.get(url,headers=headers).json()
          cidade = response['cidade']
     except:
          cidade = '405'
     return cidade


def consultar_cliente_facta(token,cpf):
     url = f'https://webservice.facta.com.br/proposta/consulta-cliente?cpf={cpf}'
     headers = {
     'Authorization': f'Bearer {token}',
     'Cookie': 'HASH_PHPSESSID=de154af5935c38cd738447d2a77f536c95072b48; PHPSESSID=i8aqihus03jlhl2ss2kb7vj822'
     }
     dados_cliente = requests.get(url,headers=headers).json()
     try:
          dados_cliente = dados_cliente['cliente'],dados_cliente = dados_cliente[0],rg = dados_cliente['RG'],orgao_emissor = dados_cliente['ORGAOEMISSOR'],estado_expedidor = dados_cliente['ESTADORG'],data_expedicao = dados_cliente['EMISSAORG'],data_expedicao=data_expedicao[0:10],data_nascimento = dados_cliente['DATANASCIMENTO'],data_nascimento=data_nascimento[0:10],sexo = dados_cliente['SEXO'],endereco = dados_cliente['ENDERECO'],num = dados_cliente['NUMERO'],bairro = dados_cliente['BAIRRO'],cidade = dados_cliente['CIDADE'],estado = dados_cliente['ESTADO'],cep = dados_cliente['CEP'],nome_mae = dados_cliente['NOMEPAI'],nome_pai = dados_cliente['NOMEMAE']
          return rg, orgao_emissor,estado_expedidor,data_expedicao,data_nascimento,sexo,endereco,num,bairro,cidade,estado,cep,nome_mae,nome_pai
     except:
          return 'erro'

if __name__ == '__main__':

     token = get_token_facta()

     # codigo_tabela,valor_operacao,coeficiente = simular_facta()

     # id_simulador = cadastrar_simulacao_facta()

     # cidade = get_cidade_facta()

     # cidade_natural = get_cidade_facta()

     # codigo_cliente = cadastrar_dados_pessoais_facta()

     # af,url = finalizar_cadastro_facta()

     # url_facta()
