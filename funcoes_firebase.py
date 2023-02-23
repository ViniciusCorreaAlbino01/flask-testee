import requests, json

url = 'https://autocontratacaocca-default-rtdb.firebaseio.com/Clientes//.json'

def criar_firebase(cpf,dados):
    url = f'https://autocontratacaocca-default-rtdb.firebaseio.com/Clientes/{cpf}/.json'
    request = requests.put(url,data=json.dumps(dados)).json()

def alterar_firebase(cpf,dados):
    url = f'https://autocontratacaocca-default-rtdb.firebaseio.com/Clientes/{cpf}/.json'
    request = requests.put(url,data = json.dumps(dados))