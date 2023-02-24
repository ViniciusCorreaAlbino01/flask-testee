from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, TelField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired, Length

class ClienteForm(FlaskForm):
    nome = StringField('Nome',validators=[DataRequired('Preencha com seu nome')])
    cpf = TelField('CPF',validators=[DataRequired('Preencha com seu cpf'), Length(min=11,max=11)] )
    telefone = TelField('Telefone',validators=[DataRequired('Preencha com seu telefone'),Length(min=11,max=11)])
    data_nascimento = DateField('data_nascimento',format='%d/%m/%Y' ,validators=[DataRequired()])
    nome_pai = StringField('nome_pai',validators=[DataRequired('Preencha com o nome do seu pai')])
    nome_mae = StringField('nome_mae',validators=[DataRequired('Preencha com o nome da sua mãe')])
    rg = DecimalField('rg',validators=[DataRequired('Preencha com o número do seu rg')])
    estado_expedidor = SelectField('Estado_expedidor', choices=[('','Selecione...'),('AC','AC'),('AL','AL'),('AP','AP'),('AM','AM'),        
    ('BA','BA'),('CE','CE'),('DF','DF'),('ES','ES'),('GO','GO'),('MA','MA'),('MT','MT'),('MS','MS'),('MG','MG'),('PA','PA'),('PB','PB'), 
    ('PR','PR'),('PE','PE'),('PI','PI'),('RJ','RJ'),('RN','RN'),('RS','RS'),('RO','RO'),('RR','RR'),('SC','SC'),('SP','SP'),('SE','SE'), 
     ('TO','TO')],validators=[DataRequired()])
    orgao_emissor = SelectField('orgao_emissor', choices=[('','Selecione...'),('SSP','SSP'),('DETRAN','DETRAN'),('CTPS','CTPS'), 
     ('Outros','Outros')],validators=[DataRequired()])
    estado = SelectField('Estado', choices=[('','Selecione...'),('AC','AC'),('AL','AL'),('AP','AP'),('AM','AM'),('BA','BA'),('CE','CE'), 
    ('DF','DF'),('ES','ES'),('GO','GO'),('MA','MA'),('MT','MT'),('MS','MS'),('MG','MG'),('PA','PA'),('PB','PB'),('PR','PR'),('PE','PE'), 
    ('PI','PI'),('RJ','RJ'),('RN','RN'),('RS','RS'),('RO','RO'),('RR','RR'),('SC','SC'),('SP','SP'),('SE','SE'),('TO','TO')],validators=[DataRequired()])
    cidade = StringField('Cidade',validators=[DataRequired('Preencha com a cidade onde você mora'), ])
    cep = TelField('cep',validators=[DataRequired('Preencha com o seu cep'),Length(min=8,max=8)])
    endereco = StringField('Logradouro',validators=[DataRequired('Preencha com o seu logradouro'), ])
    bairro = StringField('bairro',validators=[DataRequired('Preencha com o seu bairro'), ])
    num = DecimalField('num',validators=[DataRequired('Preencha com o num da sua residência'), ])
    banco = TelField('banco',validators=[DataRequired('Preencha com o codigo do seu banco'), Length(min=3,max=3)])
    agencia = TelField('agencia',validators=[DataRequired('Preencha com o numero da sua agencia'),Length(min=4,max=4) ])
    conta = DecimalField('conta',validators=[DataRequired('Preencha com o numero da sua conta'), ])
    data_expedicao = DateField('data_expedicao',format='%d/%m/%Y',validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('','Selecione...'),('Feminino','Feminino'),('Masculino','Masculino')],validators=[DataRequired()])
    tipo_conta = SelectField('tipo_conta', choices=[('','Selecione...'),(1,'Conta Corrente'),(2,'Cartão Magnético')],validators=[DataRequired()])
    especie = SelectField('especie', choices=[('','Selecione...'),('21','21 - Pensão por morte previdenciária'),('32','32 - Aposentadoria por invalidez previdenciária'),('41','41 - Aposentadoria por idade'),('42','42 - Aposentadoria por tempo de contribuição'),('46','46 - Aposentadoria por tempo de contribuição especial'),('57','57 - Aposentadoria por tempo de contribuição professores'),('87','87 - Amparo assistencial ao portador de deficiência'),('88','88 - Amparo assistencial ao idoso'),('92','92 - Aposentadoria por invalidez por acidente do trabalho'),('93','93 - Pensão por morte por acidente de trabalho')],validators=[DataRequired()])
    matricula = TelField('matricula',validators=[DataRequired('Preencha com o numero do seu benefício'),Length(min=10,max=10) ])