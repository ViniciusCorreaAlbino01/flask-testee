from flask import Flask, render_template,request,make_response,request,redirect
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, TelField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired, Length
import json
import os 
from datetime import datetime
from Funcoes_Facta import * 
from funcoes_trello import *
from funcoes_C6 import *
from funcoes_sql import * 
from funcoes_firebase import *
from form import *

app = Flask(__name__)
WTF_CSRF_ENABLED = False
app.config['WTF_CSRF_ENABLED'] = False


class Cliente():
    def __init__(self):
        self.cpf = ''

Cliente_atual = Cliente()

@app.errorhandler(404)
def erro_404(e):
    form = ClienteForm()
    return render_template('404.html',form = form)    

@app.route('/',methods =['POST','GET'])
def homepage():
    form = ClienteForm()
    try:
        Cliente_atual.cpf = request.form.get("cpf")
        Cliente_atual.data_nascimento = request.form.get("data_nascimento")
        Cliente_atual.telefone = request.form.get("telefone")
        Cliente_atual.nome = request.form.get("nome")
        verificacao =verificar_cpf(Cliente_atual.cpf)
        if verificacao == 'invalido':
            return render_template('cpf_invalido.html',form = form)
    except:
        return render_template('index.html', form=form)
    if Cliente_atual.cpf != None:
        try:
            Cliente_atual.token_facta = get_token_facta ()
            Cliente_atual.especie, Cliente_atual.salario, Cliente_atual.matricula, Cliente_atual.margem_novo = consulta_database(Cliente_atual.cpf)
        except:
            return render_template('tente_mais_tarde.html',form = form)
        try:
            Cliente_atual.taxa,Cliente_atual.codigo_tabela, Cliente_atual.valor_operacao, Cliente_atual.coeficiente =  simular_facta(Cliente_atual.token_facta,Cliente_atual.margem_novo,84,Cliente_atual.cpf,Cliente_atual.data_nascimento,Cliente_atual.especie)
        except:
            return render_template('cpf_invalido.html', form=form)
        try:
            Cliente_atual.hora =  datetime.now().strftime("%d/%m %H:%M:%S")
            Cliente_atual.card_lead = criar_card(Cliente_atual.nome,'63c6a9be9468550317b5f2fd',f'CPF: {Cliente_atual.cpf} \n Nome: {Cliente_atual.nome}  \n Data de nascimento: {Cliente_atual.data_nascimento} \n Telefone: {Cliente_atual.telefone} \n Data de entrada : {Cliente_atual.hora}')
            criar_firebase(Cliente_atual.cpf,{'CPF':Cliente_atual.cpf,'Nome':Cliente_atual.nome,'Telefone':Cliente_atual.telefone,'Data de Nascimento':Cliente_atual.data_nascimento,'Hora':Cliente_atual.hora})
        except:
            None
    if Cliente_atual.codigo_tabela != None:
            return redirect("/simulacoes")
    


@app.route('/simulacoes', methods = ['POST','GET'])
def simulacoes():
    try:
        Cliente_atual.rg, Cliente_atual.orgao_emissor,Cliente_atual.estado_expedidor,Cliente_atual.data_expedicao,Cliente_atual.data_nascimento,Cliente_atual.sexo,Cliente_atual.endereco,Cliente_atual.num,Cliente_atual.bairro,Cliente_atual.cidade,Cliente_atual.estado,Cliente_atual.cep,Cliente_atual.nome_mae,Cliente_atual.nome_pai=consultar_cliente_facta(Cliente_atual.token_facta,Cliente_atual.cpf)
    except:
        Cliente_atual.orgao_emissor = ''
        Cliente_atual.estado_expedidor = ''
        Cliente_atual.estado = ''
        Cliente_atual.sexo = ''
    if Cliente_atual.orgao_emissor == 'DETRAN':
        ClienteForm.orgao_emissor = SelectField('orgao_emissor', choices=[('DETRAN','DETRAN'),('SSP','SSP'),('CTPS','CTPS'), 
('Outros','Outros')],validators=[DataRequired()])
    elif Cliente_atual.orgao_emissor == 'SSP':
        ClienteForm.orgao_emissor = SelectField('orgao_emissor', choices=[('SSP','SSP'),('DETRAN','DETRAN'),('CTPS','CTPS'), 
('Outros','Outros')],validators=[DataRequired()])
    elif Cliente_atual.orgao_emissor == 'CTPS':
        ClienteForm.orgao_emissor = SelectField('orgao_emissor', choices=[('CTPS','CTPS'), ('SSP','SSP'),('DETRAN','DETRAN'),
('Outros','Outros')],validators=[DataRequired()])
    else:
        None
    if Cliente_atual.sexo == 'F':
        ClienteForm.sexo = SelectField('Sexo', choices=[('Feminino','Feminino'),('Masculino','Masculino')],validators=[DataRequired()]) 
    elif Cliente_atual.sexo == 'M':
        ClienteForm.sexo = SelectField('Sexo', choices=[('Masculino','Masculino'),('Feminino','Feminino')],validators=[DataRequired()])
    else: 
        None
    
    return render_template('simulacoes.html',parcela = Cliente_atual.margem_novo,valor_operacao = Cliente_atual.valor_operacao,taxa=Cliente_atual.taxa)

@app.route('/contratar', methods = ['POST','GET'])
def contratar():
    form = ClienteForm()
    try:
        Cliente_atual.nome_mae = request.form.get("nome_mae")
        Cliente_atual.nome_pai = request.form.get("nome_pai")
        Cliente_atual.rg = request.form.get("rg")
        Cliente_atual.orgao_emissor = request.form.get("orgao_emissor")
        Cliente_atual.data_expedicao = request.form.get("data_expedicao")
        Cliente_atual.estado_expedidor = request.form.get("estado_expedidor")
        Cliente_atual.sexo = request.form.get("sexo")
        Cliente_atual.cep = request.form.get("cep")
        Cliente_atual.endereco = request.form.get("endereco")
        Cliente_atual.bairro = request.form.get("bairro")
        Cliente_atual.cidade = request.form.get("cidade")
        Cliente_atual.cidade1 = request.form.get("cidade")
        Cliente_atual.estado = request.form.get("estado")
        Cliente_atual.num = request.form.get("num")
        Cliente_atual.banco = request.form.get("banco")
        Cliente_atual.agencia = request.form.get("agencia")
        Cliente_atual.conta = request.form.get("conta")
        Cliente_atual.especie = request.form.get("especie")
        Cliente_atual.matricula = request.form.get("matricula")
        Cliente_atual.tipo_conta = request.form.get("tipo_conta")
        Cliente_atual.token_facta = get_token_facta()
    except:
        None
    if Cliente_atual.nome_mae != None:
        if Cliente_atual.sexo == 'Feminino':
            Cliente_atual.sexo = 'F'
        else:
            Cliente_atual.sexo = 'M'
        try:
            Cliente_atual.id_simulador = cadastrar_simulacao_facta(Cliente_atual.token_facta,13,Cliente_atual.cpf,Cliente_atual.data_nascimento,Cliente_atual.codigo_tabela,84,Cliente_atual.valor_operacao,Cliente_atual.margem_novo,Cliente_atual.coeficiente)
        except:
            try:
                Cliente_atual.id_simulador = cadastrar_simulacao_facta(Cliente_atual.token_facta,13,Cliente_atual.cpf,Cliente_atual.data_nascimento,
                Cliente_atual.codigo_tabela,84,Cliente_atual.valor_operacao-1000,Cliente_atual.margem_novo,Cliente_atual.coeficiente)
            except:
                None

        Cliente_atual.cidade_codigo = get_cidade_facta(Cliente_atual.token_facta,Cliente_atual.estado,Cliente_atual.cidade)
        Cliente_atual.codigo_cliente = cadastrar_dados_pessoais_facta(Cliente_atual.token_facta,Cliente_atual.id_simulador,Cliente_atual.cpf,Cliente_atual.nome,Cliente_atual.sexo,1,Cliente_atual.data_nascimento,Cliente_atual.rg,Cliente_atual.estado_expedidor,Cliente_atual.orgao_emissor,Cliente_atual.data_expedicao,Cliente_atual.estado,Cliente_atual.cidade_codigo,Cliente_atual.telefone,1212,Cliente_atual.cep,Cliente_atual.endereco,Cliente_atual.num,Cliente_atual.bairro,Cliente_atual.cidade_codigo,Cliente_atual.estado,Cliente_atual.nome_mae,Cliente_atual.nome_pai,Cliente_atual.banco,Cliente_atual.agencia,Cliente_atual.conta,Cliente_atual.matricula,Cliente_atual.tipo_conta,Cliente_atual.especie,Cliente_atual.banco,Cliente_atual.agencia,Cliente_atual.conta)
        try:
            Cliente_atual.ade,Cliente_atual.link = finalizar_cadastro_facta(Cliente_atual.token_facta,Cliente_atual.codigo_cliente,Cliente_atual.id_simulador)
            url_facta(Cliente_atual.token_facta,Cliente_atual.ade)
        except:
            None
        if 'rg' in Cliente_atual.codigo_cliente:
            return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = '',nome_mae = Cliente_atual.nome_mae,nome_pai = Cliente_atual.nome_pai,orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = Cliente_atual.data_expedicao, estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = Cliente_atual.cep,endereco=Cliente_atual.endereco,bairro=Cliente_atual.bairro,cidade=Cliente_atual.cidade,estado=Cliente_atual.estado,num = Cliente_atual.num)
        if 'data_expedicao' in Cliente_atual.codigo_cliente:
            return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = Cliente_atual.rg,nome_mae = Cliente_atual.nome_mae,nome_pai = Cliente_atual.nome_pai,orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = '', estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = Cliente_atual.cep,endereco=Cliente_atual.endereco,bairro=Cliente_atual.bairro,cidade=Cliente_atual.cidade,estado=Cliente_atual.estado,num = Cliente_atual.num)
        if 'cidade' in Cliente_atual.codigo_cliente:
            return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = Cliente_atual.rg,nome_mae = Cliente_atual.nome_mae,nome_pai = Cliente_atual.nome_pai,orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = Cliente_atual.data_expedicao, estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = Cliente_atual.cep,endereco=Cliente_atual.endereco,bairro=Cliente_atual.bairro,cidade='',estado=Cliente_atual.estado,num = Cliente_atual.num)
        if 'cep' in Cliente_atual.codigo_cliente:
            return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = Cliente_atual.rg,nome_mae = Cliente_atual.nome_mae,nome_pai = Cliente_atual.nome_pai,orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = Cliente_atual.data_expedicao, estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = '',endereco=Cliente_atual.endereco,bairro=Cliente_atual.bairro,cidade=Cliente_atual.cidade,estado=Cliente_atual.estado,num = Cliente_atual.num)
        if 'endereco' in Cliente_atual.codigo_cliente:
            return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = Cliente_atual.rg,nome_mae = Cliente_atual.nome_mae,nome_pai = Cliente_atual.nome_pai,orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = Cliente_atual.data_expedicao, estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = Cliente_atual.cep,endereco='',bairro=Cliente_atual.bairro,cidade=Cliente_atual.cidade,estado=Cliente_atual.estado,num = Cliente_atual.num)
        if 'bairro' in Cliente_atual.codigo_cliente:
            return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = Cliente_atual.rg,nome_mae = Cliente_atual.nome_mae,nome_pai = Cliente_atual.nome_pai,orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = Cliente_atual.data_expedicao, estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = Cliente_atual.cep,endereco=Cliente_atual.endereco,bairro='',cidade=Cliente_atual.cidade,estado=Cliente_atual.estado,num = Cliente_atual.num)
        if 'numero' in Cliente_atual.codigo_cliente:
            return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = Cliente_atual.rg,nome_mae = Cliente_atual.nome_mae,nome_pai = Cliente_atual.nome_pai,orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = Cliente_atual.data_expedicao, estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = Cliente_atual.cep,endereco=Cliente_atual.endereco,bairro=Cliente_atual.bairro,cidade=Cliente_atual.cidade,estado=Cliente_atual.estado,num = '')
        if 'nome_mae' in Cliente_atual.codigo_cliente:
            return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = Cliente_atual.rg,nome_mae = '',nome_pai = Cliente_atual.nome_pai,orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = Cliente_atual.data_expedicao, estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = Cliente_atual.cep,endereco=Cliente_atual.endereco,bairro=Cliente_atual.bairro,cidade=Cliente_atual.cidade,estado=Cliente_atual.estado,num = Cliente_atual.num)
        if 'nome_pai' in Cliente_atual.codigo_cliente:
            return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = Cliente_atual.rg,nome_mae = Cliente_atual.nome_mae,nome_pai = '',orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = Cliente_atual.data_expedicao, estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = Cliente_atual.cep,endereco=Cliente_atual.endereco,bairro=Cliente_atual.bairro,cidade=Cliente_atual.cidade,estado=Cliente_atual.estado,num = Cliente_atual.num)
        if Cliente_atual.link != None:
            return redirect('/formalizacao')
    else:
        if Cliente_atual.nome_mae != None:
            try:
                return render_template('pag2.html', form = form, nome=Cliente_atual.nome,rg = Cliente_atual.rg,nome_mae = Cliente_atual.nome_mae,nome_pai = Cliente_atual.nome_pai,orgao_emissor = Cliente_atual.orgao_emissor,data_expedicao = Cliente_atual.data_expedicao, estado_expedidor = Cliente_atual.estado_expedidor, sexo = Cliente_atual.sexo,cep = Cliente_atual.cep,endereco=Cliente_atual.endereco,bairro=Cliente_atual.bairro,cidade=Cliente_atual.cidade,estado=Cliente_atual.estado,num = Cliente_atual.num)
            except:
                return render_template('pag2.html',form = form)
        else:
            return render_template('Erro.html')
    
        
            

@app.route('/formalizacao',methods=['POST','GET'])
def cadastrar():    
    
    try:
        criar_card(Cliente_atual.nome,'63c53f3550441b0c74663ac4',f'CPF: {Cliente_atual.cpf} \n Nome: {Cliente_atual.nome}  \n Telefone: {Cliente_atual.telefone} \n Data de Nascimento: {Cliente_atual.data_nascimento} \n Sexo: {Cliente_atual.sexo} \n RG: {Cliente_atual.rg} \n Órgão Emissor: {Cliente_atual.orgao_emissor} \n Estado Expedidor: {Cliente_atual.estado_expedidor} \n Data de Emissão: {Cliente_atual.data_expedicao}\n Nome da Mãe: {Cliente_atual.nome_mae}\n Nome do Pai: {Cliente_atual.nome_pai}\n CEP: {Cliente_atual.cep} \n Endereço: {Cliente_atual.endereco} \n Número: {Cliente_atual.num} \n Bairro: {Cliente_atual.bairro} \n Cidade: {Cliente_atual.cidade} \n Estado: {Cliente_atual.estado} \n Banco: {Cliente_atual.banco} \n Agência: {Cliente_atual.agencia} \n Conta: {Cliente_atual.conta} \n Link: {Cliente_atual.link} \n ADE: {Cliente_atual.ade}')
        alterar_card(Cliente_atual.card_lead,f'CPF: {Cliente_atual.cpf} \n Nome: {Cliente_atual.nome}  \n Telefone: {Cliente_atual.telefone} \n Data de Nascimento: {Cliente_atual.data_nascimento} \n Sexo: {Cliente_atual.sexo} \n RG: {Cliente_atual.rg} \n Órgão Emissor: {Cliente_atual.orgao_emissor} \n Estado Expedidor: {Cliente_atual.estado_expedidor} \n Data de Emissão: {Cliente_atual.data_expedicao}\n Nome da Mãe: {Cliente_atual.nome_mae}\n Nome do Pai: {Cliente_atual.nome_pai}\n CEP: {Cliente_atual.cep} \n Endereço: {Cliente_atual.endereco} \n Número: {Cliente_atual.num} \n Bairro: {Cliente_atual.bairro} \n Cidade: {Cliente_atual.cidade1} \n Estado: {Cliente_atual.estado} \n Banco: {Cliente_atual.banco} \n Agência: {Cliente_atual.agencia} \n Conta: {Cliente_atual.conta} \n Link: {Cliente_atual.link} \n ADE: {Cliente_atual.ade} \n Data de entrada: {Cliente_atual.hora}',Cliente_atual.nome+"✔️ Digitado")
        alterar_firebase(Cliente_atual.cpf,{'CPF':Cliente_atual.cpf,'Nome':Cliente_atual.nome,'Telefone':Cliente_atual.telefone,'Data de Nascimento':Cliente_atual.data_nascimento,'Sexo':Cliente_atual.sexo,'RG':Cliente_atual.rg,'Órgão Emissor':Cliente_atual.orgao_emissor,'Estado Expedidor':Cliente_atual.estado_expedidor,'Data de Emissão':Cliente_atual.data_expedicao,'Nome da mãe':Cliente_atual.nome_mae,'Nome do Pai':Cliente_atual.nome_pai,'CEP':Cliente_atual.cep,'Endereço':Cliente_atual.endereco,'Número':Cliente_atual.num,'Bairro':Cliente_atual.bairro,'Cidade':Cliente_atual.cidade,'Estado':Cliente_atual.estado,'Banco':Cliente_atual.banco,'Agência':Cliente_atual.agencia,'Conta':Cliente_atual.conta,'Link':Cliente_atual.link,'ADE':Cliente_atual.ade, 'Hora':Cliente_atual.hora})
    except:
        None
    return render_template('pag4.html', link = Cliente_atual.link)

    

#colocar o site no ar
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5000)



