import requests, json


def token_c6():
    url = "https://marketplace-proposal-service-api-h.c6bank.info/auth/token"

    payload='username=37000285800_001251&password=c6Bank%401234'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    token = response['access_token']
    return token

def simular_c6(cpf,data_nascimento,uf,prazo,token):
    url = "https://marketplace-proposal-service-api-h.c6bank.info/marketplace/proposal/fgts/simulation"

    payload = json.dumps({
    "simulation_type": "POR_QUANTIDADE_DE_PARCELAS",
    "table_code": "000008",
    "tax_identifier": cpf,
    "birth_date": data_nascimento,
    "federation_unit": uf,
    "promoter_code": "001251",
    "installment_quantity": prazo
    })
    headers = {
    'Authorization': token,
    'Accept': 'application/vnd.c6bank_error_data_v2+json',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

def digitar_c6(cpf,nome,tipo_documento,num_documento,uf_documento,expedicao_documento,data_nascimento,genero,nome_mae,ddd,telefone,rua,num,bairro,cidade,uf,banco,agencia,tipo_conta,conta,digito_conta,token):
    url = "https://marketplace-proposal-service-api-h.c6bank.info/marketplace/proposal/fgts"

    payload = json.dumps({
    "table_code": "000008",
    "formalization_subtype": "DIGITAL_WEB",
    "requested_amount": "1000",
    "origin": {
        "promoter_code": "001251",
        "typist_code": "",
        "tax_identifier_of_certified_agent": ""
    },
    "client": {
        "tax_identifier": cpf,
        "name": nome,
        "nationality_code": "01",
        "document_type": tipo_documento,
        "document_number": num_documento,
        "document_federation_unit": uf_documento,
        "document_issuance_date": expedicao_documento,
        "birth_date": data_nascimento,
        "gender": genero,
        "income_amount": "5000",
        "mother_name": nome_mae,
        "mobile_phone_area_code": ddd,
        "mobile_phone_number": telefone,
        "marital_status": "Solteiro",
        "pep": "Nao",
        "email": "",
        "address": {
        "street": rua,
        "number": num,
        "neighborhood": bairro,
        "city": cidade,
        "federation_unit": uf,
        "zip_code": cpf
        },
        "bank_data": {
        "bank_code": banco,
        "agency_number": agencia,
        "account_type": tipo_conta,
        "account_number": conta,
        "account_digit": digito_conta
        }
    }
    })
    headers = {
    'Authorization': token,
    'Accept': 'application/vnd.c6bank_error_data_v2+json',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
