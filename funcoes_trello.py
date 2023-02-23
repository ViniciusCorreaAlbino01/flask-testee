import requests,json

id_contratos = '63c53f3550441b0c74663abc'
id_em_preenchimento = '63c53f3550441b0c74663ac3'
id_concluido = '63c53f3550441b0c74663ac4'
id_formalizado = '63c53f3550441b0c74663ac5'
id_leads = '63c53f212def290016c959fe'
id_novo_lead = '63c6a9be9468550317b5f2fd'
id_quente = '63c53f212def290016c95a05'
id_morno = '63c53f212def290016c95a06'
id_frio = '63c53f212def290016c95a07'
id_fechado_ganho = '63c6a9c8d1a75402c496098f'
id_fechado_perdido = '63c6a9d026053002e63abce4'

def criar_card(nome,coluna,obs):
        criar_card=requests.post(f'https://api.trello.com/1/cards?idList={coluna}&key=6556d69c6d67e64e35c5dac7f07b5949&token=ATTAbc4b31d097783681bc8ba2b35fa5ff56663542f6597807725e4d4f18895a8ad07B76588C&name={nome}&desc={obs}').json()
        id_card = criar_card['id']
        return id_card

def alterar_card(id_card,obs,nome):
     alterar_card = requests.put(f'https://api.trello.com/1/cards/{id_card}?desc={obs}&key=6556d69c6d67e64e35c5dac7f07b5949&token=ATTAbc4b31d097783681bc8ba2b35fa5ff56663542f6597807725e4d4f18895a8ad07B76588C&name={nome}').json()

def deletar_card(id_deletar):
     deletar_card = requests.delete(f'https://api.trello.com/1/cards/{id_deletar}?&key=6556d69c6d67e64e35c5dac7f07b5949&token=ATTAbc4b31d097783681bc8ba2b35fa5ff56663542f6597807725e4d4f18895a8ad07B76588C')


def criar_dados(dados):
    request_cliente = requests.post(f'https://autocontratacaocca-default-rtdb.firebaseio.com/Clientes/.json',data = json.dumps(dados))
    id_cliente = request_cliente.json()['name']
    return id_cliente

def alterar_dados(dados,id_cliente):
     request_cliente = requests.put(f'https://autocontratacaocca-default-rtdb.firebaseio.com/Clientes/{id_cliente}/.json',data = json.dumps(dados))