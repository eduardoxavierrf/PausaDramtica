import os

from flask import Flask, render_template, request, redirect, url_for

from models.usuario import Usuario
from models.models import Model
from models.ponto_turistico import PontoTuristico
from models.passeio import Passeio
import sqlite3

import sqlite3

app = Flask(__name__)

vLogin = 0
usr = ''
usrList = ''
resultado = ''

@app.route('/')
def main():
    return redirect(url_for('index'))

@app.route('/pesquisa', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        global resultado
        local = request.form['Local']
        busca = Model(tabela='pontos_turisticos')
        resultado = busca.get(lugar = local)
        return redirect(url_for('index'))

@app.route('/like', methods=['POST'])
def like():
    if request.method == 'POST':
        ponto = request.form['pontolike']
        id_ponto = int(request.form['id_ponto'])
        busca = Model(tabela='pontos_turisticos')
        resultado = busca.get(name=ponto)

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
        '''
        SELECT * FROM like WHERE id_ponto=? AND id_usuarios=? AND likeOrDislike=0
        ''', (id_ponto, usrList[0][0])
        )
        lista1 = cursor.fetchall()
        connection.close()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
        '''
        SELECT * FROM like WHERE id_ponto=? AND id_usuarios=? AND likeOrDislike=1
        ''', (id_ponto, usrList[0][0])
        )
        lista = cursor.fetchall()
        connection.commit()
        connection.close()
        
        if len(lista) == 0:
            like = resultado[0][5] + 1
            dislike = resultado[0][6]
            if len(lista1) != 0:
                dislike = resultado[0][6] - 1
                connection = sqlite3.connect('database.db')
                cursor = connection.cursor()
                cursor.execute(
                '''
                UPDATE like SET likeOrDislike=1 WHERE id_ponto=? AND id_usuarios=?
                ''', (id_ponto, usrList[0][0])
                )
                connection.commit()
                connection.close()
            else:
                tabelaDislike = Model(tabela='like', id_usuarios= usrList[0][0], id_ponto= id_ponto, likeOrDislike= 1)
                tabelaDislike.save()

            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute(
            '''
            UPDATE pontos_turisticos set like=?, dislike=? where name=?
            ''', (like, dislike, ponto)
            )
            connection.commit()
            connection.close()
        return redirect(url_for('index'))

@app.route('/dislike', methods=['POST'])
def dislike():
    if request.method == 'POST':
        ponto = request.form['pontodislike']
        id_ponto = int(request.form['id_ponto'])
        busca = Model(tabela='pontos_turisticos')
        resultado = busca.get(name=ponto)

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        lista1 = cursor.execute(
        '''
        SELECT * FROM like WHERE id_ponto=? AND id_usuarios=? AND likeOrDislike=0
        ''', (id_ponto, usrList[0][0])
        ).fetchall()
        lista = cursor.execute(
        '''
        SELECT * FROM like WHERE id_ponto=? AND id_usuarios=? AND likeOrDislike=1
        ''', (id_ponto, usrList[0][0])
        ).fetchall()
        connection.commit()
        connection.close()
        
        if len(lista1) == 0:

            dislike = resultado[0][6] + 1
            like = resultado[0][5]
            if len(lista) != 0:
                like = resultado[0][5] - 1
                connection = sqlite3.connect('database.db')
                cursor = connection.cursor()
                cursor.execute(
                '''
                UPDATE like SET likeOrDislike=0 WHERE id_ponto=? AND id_usuarios=?
                ''', (id_ponto, usrList[0][0])
                )
                connection.commit()
                connection.close()
            else:
                tabelaDislike = Model(tabela='like', id_usuarios= usrList[0][0], id_ponto= id_ponto, likeOrDislike= 0)
                tabelaDislike.save()
            print(usrList[0][0])
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute(
            '''
            UPDATE pontos_turisticos set like=?, dislike=? where name=?
            ''', (like, dislike, ponto)
            )
            connection.commit()
            connection.close()
        return redirect(url_for('index'))


@app.route('/index')
def index():
    pontos = Model(tabela='pontos_turisticos')
    pts = pontos.get_all()
    global resultado
    if len(resultado) != 0:
        pts = resultado
        resultado = pontos.get_all()
    return render_template('index.html', len=len(pts), pontos= pts, vLogin=vLogin, usr= usr, usrList=usrList)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    global vLogin
    if vLogin == 0:
        if request.method == 'POST':
            username = request.form['username']
            senha = request.form['senha']

            user = Usuario(tabela='usuarios', username=username, senha=senha)
            validate = user.autenticar()

            if validate:
                #global vLogin
                global usr
                global usrList
                usr = username
                usuario = Model(tabela='usuarios')
                usrList = usuario.get(username=username)
                vLogin = 1
                return redirect(url_for('index'))
            else:
                erro = 'Login ou senha incorretos'
                return render_template('Login.html', erro=erro)
        if request.method == 'GET':
            return render_template('Login.html')
    else:
        #global vLogin
        vLogin = 0
        return redirect(url_for('index'))


@app.route('/registrar', methods = ['POST', 'GET'])
def registrar():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        email = request.form['email']
        tipo = request.form['tipo']

        user = Usuario(tabela='usuarios', username=username, senha=senha, email=email, tipo=tipo)
        validate = user.registrar()

        if validate:
            return redirect(url_for('login'))
        else:
            erro= 'Usuario ja existe'
            return render_template('registro.html', erro=erro)
    if request.method == 'GET':
        return render_template('registro.html')

@app.route('/criar', methods = ['POST', 'GET'])
def criar():
    if request.method == 'POST':
        name = request.form['name']
        descricao = request.form['descricao']
        lugar = request.form['lugar']
        image = request.files['foto']
        #app.config["IMAGE_UPLOADS"] = "C:\Users\cmore\Documents\env_trabalho\pausa-dramatica\static\img"
        #image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.a))

        user = PontoTuristico(tabela='pontos_turisticos', name=name, imagem="a", descricao=descricao, lugar=lugar, like=0, dislike=0)
        validate = user.criarPonto()  

        if validate:
            return redirect(url_for('index'))
        else:
            return render_template('criar.html')
    if request.method == 'GET':
        return render_template('criar.html')

@app.route('/<name>', methods = ['POST', 'GET'])
def ponto(name):
    ponto = Model(tabela='pontos_turisticos')
    pt = ponto.get(name=name)
    passeio = Model(tabela='passeios')
    dados = passeio.get(ponto=name)
    return render_template('ponto.html', len=len(dados), dados=dados, pontos= pt, vLogin=vLogin, usr= usr, usrList=usrList)

@app.route('/oferecer', methods = ['POST', 'GET'])
def oferecer():
    if request.method == 'POST':
        ponto = request.form['ponto']
        data = request.form['data']
        guia=usr

        user = Passeio(tabela='passeios', guia=guia, ponto=ponto, data=data)
        validate = user.oferecerPasseio()  

        if validate:
            return redirect(url_for('index'))
        else:
            return render_template('oferecer.html')
    if request.method == 'GET':
        return render_template('oferecer.html')

@app.route('/perfil', methods = ['POST', 'GET'])
def perfil():
    """connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    lista = cursor.execute(
    '''
    SELECT * FROM like WHERE id_ponto=? AND id_usuarios=? AND likeOrDislike=1
    ''', (id_ponto, usrList[0][0])
    ).fetchall()
    connection.commit()
    connection.close()"""
    a = Model(tabela='like')
    b = a.get(id_usuarios=usrList[0][0])
    pontos = Model(tabela='pontos_turisticos')
    pts = pontos.get_all()
    return render_template('perfil.html', b=b, len=len(pts), len1=len(b), pontos= pts, vLogin=vLogin, usr= usr, usrList=usrList)

if __name__ == '__main__':
    app.run(debug=True)

