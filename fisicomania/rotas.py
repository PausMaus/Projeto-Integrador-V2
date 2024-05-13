from flask import render_template, redirect, url_for, flash, request, abort
from fisicomania import app, database, bcrypt
from fisicomania.forms import FormLogin, FormCriarConta, FormEditarPerfil, \
    FormEditarAluno, FormCriarAluno, FormCriarPosts
from fisicomania.models import Usuario,Aluno,Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

@app.route('/')
@login_required
def homepage():
    return redirect(url_for('login'))

#--------------------------------------------------------------------------------------------------------#

@app.route('/inicio')
@login_required
def homepage1():
    post = Post.query.order_by(Post.id.desc())


    return render_template('home.html', post=post)
#--------------------------------------------------------------------------------------------------------#

@app.route('/aluno', methods=['GET', 'POST'])
@login_required
def aluno():

    lista_alunos = Aluno.query.all()






    return render_template('alunos.html', lista_alunos=lista_alunos,aluno=Aluno )

def atualizar_plano(form):
    lista_plano =[]
    for campo in form:
        if campo.data:
            if 'plano_' in campo.name:
                lista_plano.append(campo.label.text)


    return ';'.join(lista_plano)

def atualizar_plano2(form):
    lista_plano1 =[]
    for campo in form:
        if campo.data:
            if 'planos_' in campo.name:
                lista_plano1.append(campo.label.text)


    return ';'.join(lista_plano1)



@app.route('/criar/aluno', methods=['GET', 'POST'])
@login_required
def criar_aluno():
    form = FormCriarAluno()

    if form.validate_on_submit():
        aluno = Aluno(nome=form.nome.data, email=form.email.data, contato=form.contato.data, mensalidade=form.mensalidade.data, autor=current_user)
        aluno.plano = atualizar_plano(form)
        aluno.planoIn = atualizar_plano2(form)


        database.session.add(aluno)
        database.session.commit()
        flash('Aluno Criado com Sucesso', 'alert-success')
        return redirect(url_for('aluno'))


    return render_template('criar_aluno.html',  form=form)


def atualizar_plano1(form6):
    lista_plano =[]
    for campo in form6:
        if campo.data:
            if 'plano_' in campo.name:
                lista_plano.append(campo.label.text)


    return ';'.join(lista_plano)

def atualizar_plano3(form6):
    lista_plano3 =[]
    for campo in form6:
        if campo.data:
            if 'planos_' in campo.name:
                lista_plano3.append(campo.label.text)


    return ';'.join(lista_plano3)
@app.route('/aluno/<aluno_id>', methods=['GET', 'POST'])
@login_required
def editar_aluno(aluno_id):
    aluno_ed= Aluno.query.get(aluno_id)
    if current_user == aluno_ed.autor:
        form6 = FormCriarAluno()
        form7 =FormEditarAluno
        if request.method =='GET':
            form6.nome.data = aluno_ed.nome
            form6.email.data = aluno_ed.email
            form6.contato.data = aluno_ed.contato


        elif form6.validate_on_submit():
            aluno_ed.nome = form6.nome.data
            aluno_ed.email = form6.email.data
            aluno_ed.contato = form6.contato.data
            aluno_ed.plano = atualizar_plano1(form6)
            aluno_ed.planoIn = atualizar_plano3(form6)

            database.session.commit()
            flash('Aluno atualizado com Sucesso', 'alert-success')
            return redirect(url_for('aluno'))


    else:
        form6 =None
    return render_template('editar_aluno.html', aluno_ed=aluno_ed, form6=form6, aluno=aluno)


@app.route('/aluno/<aluno_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_aluno(aluno_id):
    aluno_ed= Aluno.query.get(aluno_id)
    if current_user == aluno_ed.autor:
        database.session.delete(aluno_ed)
        database.session.commit()
        flash('Aluno excluido com sucesso', 'alert-danger')
        return redirect(url_for('aluno'))
    else:
        abort(403)



#--------------------------------------------------------------------------------------------------------#

@app.route('/criar/post', methods=['GET', 'POST'])
@login_required
def criar_post():
    form4 = FormCriarPosts()
    if form4.validate_on_submit():
        post = Post(titulo=form4.titulo.data, corpo=form4.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Recado Criado com Sucesso', 'alert-success')
        return redirect(url_for('homepage1'))


    return render_template('criar_post.html', form4=form4)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post =Post.query.get(post_id)
    if current_user == post.autor:
        form5 = FormCriarPosts()
        if request.method =='GET':
            form5.titulo.data = post.titulo
            form5.corpo.data = post.corpo
        elif form5.validate_on_submit():
            post.titulo = form5.titulo.data
            post.corpo = form5.corpo.data
            database.session.commit()
            flash('Post atualizado com Sucesso', 'alert-success')
            return redirect(url_for('homepage1'))

    else:
        form5 =None
    return render_template('editar_post.html', post=post, form5=form5)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluido com sucesso', 'alert-danger')
        return redirect(url_for('homepage1'))
    else:
        abort(403)

#--------------------------------------------------------------------------------------------------------#

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login= FormLogin()
    form_criar_conta= FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember = form_login.lembrar_dados.data)
            flash(f'Login efetuado com sucesso no e-mail:{form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return render_template('home.html')
        else:
            flash('Falha no login . E-mail ou senha Incorretos', 'alert-danger')


    if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta Criada para o e-mail:{form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)
#--------------------------------------------------------------------------------------------------------#

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout efetuado com sucesso.', 'alert-success')
    return redirect(url_for('homepage1'))

#--------------------------------------------------------------------------------------------------------#

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='imagens/foto_perfil/{}'.format(current_user.foto_perfil))


    return render_template('perfil.html', foto_perfil=foto_perfil)






def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/imagens/foto_perfil', nome_arquivo)
    tamanho = (500, 500)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form1):
    lista_curso =[]
    for campo in form1:
        if 'alunos_' in campo.name:
            if campo.data:
                lista_curso.append(campo.label.text)
    return ';'.join(lista_curso)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form1 = FormEditarPerfil()
    if form1.validate_on_submit():
        current_user.email = form1.email.data
        current_user.username = form1.username.data
        if form1.foto_perfil.data:
            nome_imagem = salvar_imagem(form1.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form1)

        database.session.commit()
        flash("Perfil atualizado com sucesso", "alert-success")
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form1.email.data = current_user.email
        form1.username.data = current_user.username
    foto_perfil = url_for('static', filename='imagens/foto_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form1=form1)


#--------------------------------------------------------------------------------------------------------#


@app.route('/tabela')
@login_required
def tabela():
    form9=FormCriarAluno
    lista_alunos = Aluno.query.all()
    Inativo = Aluno.query.filter_by(planoIn='Aluno Inativo').count()
    Ativo = Aluno.query.filter_by(plano='Aluno Ativo').count()
    total_alunos = Inativo + Ativo
    mensalidade=Aluno.query.filter_by(mensalidade='Mensalidade').count()
    print(mensalidade)

    return render_template('tabela.html' , lista_alunos=lista_alunos, aluno=Aluno, total_alunos=total_alunos , Ativo=Ativo, Inativo=Inativo, mensalidade=mensalidade, form9=form9)