import mysql.connector,sys


def consulta_database(cpf):
    cpf = cpf.lstrip('0')
    try:
        conexao_railway = mysql.connector.connect(
            host = 'localhost',
            port = '3306',
            user = 'root',
            password = '',
            database = 'Bases'
        )

        cursor_railway = conexao_railway.cursor()
        comando = f'Select * from Clientes where cpf = {cpf}'
        cursor_railway.execute(comando)
        rows = cursor_railway.fetchall()
    
        dados = rows[0]
        especie = dados[6]
        matricula = dados[7]
        salario = dados[8]
        margem_novo = dados[9]
    except:
        especie = '21'
        salario = 1212
        matricula = '1234123412'
        margem_novo = 424.20
    return  especie,salario,matricula,margem_novo

def verificar_cpf(cpf):
    i = 0
    cpfdv1 = int(cpf[9:10])
    cpfdv2 = int(cpf[10:11])
    numdv1 = 0
    numdv2 = 0
    for i in range(1,10):
        numdv1 = numdv1 + int(cpf[i-1:i]) * i
    numdv1 = numdv1 % 11
    if numdv1 == 10:
        numdv1 = 0
    if numdv1 != cpfdv1:
        return 'invalido'
    for i in range(2,11):
        numdv2 = numdv2 + int(cpf[i-1:i]) * (i-1)
    numdv2 = numdv2 % 11
    if numdv2 == 10 :
        numdv2 = 0
    if numdv2 != cpfdv2:
        return 'invalido'
    if numdv1 == cpfdv1 and numdv2 == cpfdv2:
        return 'valido'
    
cpf = verificar_cpf('12312312312')
cpf
