from fisicomania import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username= database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    post = database.relationship('Post', backref='autor', lazy=True )
    aluno = database.relationship('Aluno', backref='autor', lazy=True)



    def contar_alunos(self):
        return len(self.aluno)
    def contar_inativos(self):
        #Inativo = Aluno.query.filter_by(planoIn='Aluno Inativo').all()
        Inativo = Aluno.query.filter_by(id_usuario=self.id, planoIn='Aluno Inativo').count()


        return (Inativo)

    def contar_ativos(self):
        Ativo = Aluno.query.filter_by(id_usuario=self.id, plano='Aluno Ativo').count()

        return (Ativo)




class Aluno(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    contato = database.Column(database.String, nullable=False)
    mensalidade = database.Column(database.Integer, nullable=False)
    plano = database.Column(database.String, nullable=False, default='Não Informado')
    planoIn = database.Column(database.String, nullable=False, default='Não Informado')
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)



class Post (database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.Integer, nullable=False)
    corpo = database.Column(database.Integer, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

class tabela(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    contato = database.Column(database.String, nullable=False)
    plano = database.Column(database.String, nullable=False, default='Não Informado')
    planoIn = database.Column(database.String, nullable=False, default='Não Informado')
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)


