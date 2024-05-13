from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\Paus Maus\Nuvem\OneDrive\Trabalho\Univesp\venv\ProjetoIntegrador\instance\ProjetoIntegrador.projetointegrador.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class tabela(db.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    contato = database.Column(database.String, nullable=False)
    plano = database.Column(database.String, nullable=False, default='Não Informado')
    planoIn = database.Column(database.String, nullable=False, default='Não Informado')
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)



if __name__ == '__main__':
    app.run(debug=True)
