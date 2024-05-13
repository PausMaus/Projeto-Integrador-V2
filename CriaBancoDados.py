from fisicomania import app, database
from fisicomania.models import Usuario, Aluno

# Comandos para deletar e recriar o Banco de Dados
with app.app_context():
    #database.drop_all()
    database.create_all()



# Comando para verificar os usuarios no Banco de Dados
#with app.app_context():
    #teste = Usuario.query.all()
    #resp = teste.email
    #senha = teste.senha
    #usuario = Usuario.query.filter_by(email='cunhacalil@gmail.com'). first()
    #cursos = usuario.cursos

#     meus_usuarios = Usuario.query.all()
    #print(cursos)
