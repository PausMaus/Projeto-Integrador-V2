from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fisicomania.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email =StringField('E-mail', validators=[DataRequired(), Email()])
    senha =PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirmacao_senha =PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta =SubmitField('Criar Conta')
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email ja cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login= SubmitField('Fazer Login')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField("Atualizar Foto de Perfil", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    botao_submit_editar_perfil= SubmitField('Salvar Alterações')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("Já existe um usuário com este e-mail. Cadastre outro e-mail.")

class FormCriarAluno(FlaskForm):
    nome =StringField('Nome', validators=[DataRequired()])
    email =StringField('E-mail', validators=[DataRequired()])
    contato = StringField('Contato', validators=[DataRequired()])
    mensalidade = StringField('Mensalidade', validators=[DataRequired()])


    plano_at = BooleanField('Aluno Ativo')
    planos_in = BooleanField('Aluno Inativo')

    botao_submit = SubmitField('Criar Aluno')
    botao_submit1 = SubmitField('Editar Aluno')

class FormEditarAluno(FlaskForm):
        nome = StringField('Nome', validators=[DataRequired()])
        email = StringField('E-mail', validators=[DataRequired()])
        contato = StringField('Contato', validators=[DataRequired()])

        aluno_at = BooleanField('Aluno Ativos')
        alunos_in = BooleanField('Aluno Inativos')

        botao_submit = SubmitField('Criar Assunto')

class FormCriarPosts(FlaskForm):
    titulo = StringField('Titulo do assunto', validators=[DataRequired(), Length(2,50)])
    corpo =  TextAreaField('Escreva seu assunto Aqui', validators=[DataRequired()])
    botao_ok = SubmitField('Criar Assunto')





