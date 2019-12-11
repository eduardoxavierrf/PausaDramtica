import os

from datetime import datetime
#from datetime.parser import parse

from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, url_for

from models.usuario import Usuario
from models.models import Model
from models.ponto_turistico import PontoTuristico
from models.passeio import Passeio

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

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/criar', methods = ['POST', 'GET'])
def criar():
    app.config["IMAGE_UPLOADS"] = "C:/Users/cmore/Documents/env_trabalho/pausa-dramatica/static/img"
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
    if request.method == 'POST':
        if request.files:
            name = request.form['name']
            descricao = request.form['descricao']
            lugar = request.form['lugar']
            image = request.files['foto']
            if image.filename == '':
                return render_template('criar.html')
            if allowed_image(image.filename):
                if ".jpg" in image.filename:
                    image.filename = name + '.jpg'
                if ".jpeg" in image.filename:
                    image.filename = name + '.jpeg'
                if ".png" in image.filename:
                    image.filename = name + '.png'
                image.filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                
                user = PontoTuristico(tabela='pontos_turisticos', name=name, imagem=image.filename, descricao=descricao, lugar=lugar, like=0, dislike=0)
                validate = user.criarPonto()  

                if validate:
                    return redirect(url_for('index'))
                else:
                    return render_template('criar.html')
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
    passeio1 = Model(tabela='passeios1')
    dados1 = [None] * len(dados)
    vLen = [None] * len(dados)
    d = [None] * len(dados)
    now = datetime.now()
    n = [now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")]
    for i in range(len(dados)):
        dados1[i] = passeio1.get(id_passeio=dados[i][0])
        vLen[i] = len(dados1[i])
        date = datetime.strptime(dados[i][3], '%Y-%m-%d').date()
        date1 = date.strftime("%x")
        now1 = now.strftime("%x")
        if date1 > now1:
            d[i] = 1
        else:
            d[i] = 0
    return render_template('ponto.html', len=len(dados), dados=dados, now=now, n=n, d=d, dados1=dados1, len1=len(dados1), vLen=vLen, pontos= pt, vLogin=vLogin, usr= usr, usrList=usrList)

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

@app.route('/likes', methods = ['POST', 'GET'])
def perfil():
    a = Model(tabela='like')
    b = a.get(id_usuarios=usrList[0][0])
    pontos = Model(tabela='pontos_turisticos')
    pts = pontos.get_all()
    return render_template('likes.html', b=b, len=len(pts), len1=len(b), pontos= pts, vLogin=vLogin, usr= usr, usrList=usrList)

@app.route('/passeios', methods = ['POST', 'GET'])
def passeios():
    if usrList[0][4] == 'Guia':

        guia = usr
        passeio = Model(tabela='passeios')
        dados = passeio.get(guia=guia)
        passeio1 = Model(tabela='passeios1')
        dados1 = [None] * len(dados)
        vLen = [None] * len(dados)
        d = [None] * len(dados)
        now = datetime.now()
        n = [now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")]
        for i in range(len(dados)):
            dados1[i] = passeio1.get(id_passeio=dados[i][0])
            vLen[i] = len(dados1[i])
            date = datetime.strptime(dados[i][3], '%Y-%m-%d').date()
            date1 = date.strftime("%x")
            now1 = now.strftime("%x")
            if date1 > now1:
                d[i] = 1
            else:
                d[i] = 0
        return render_template('passeios.html', len=len(dados), dados=dados, now=now, n=n, d=d, dados1=dados1, len1=len(dados1), vLen=vLen, vLogin=vLogin, usr= usr, usrList=usrList)

    if usrList[0][4] == 'Turista':
        a = Model(tabela='passeios1')
        b = a.get(name_turista=usr)
        a1 = Model(tabela='passeios')
        lenV = [None] * len(b)
        V = [None] * len(b)
        for i in range(len(b)):
            V[i] = a1.get(id=b[i][1])
            lenV[i] = len(V[i])
        print(lenV)
        return render_template('passeios.html', V=V, len=len(b), lenV=lenV, vLogin=vLogin, usr= usr, usrList=usrList)

@app.route('/adicionar', methods = ['POST', 'GET'])
def adicionar():
    if request.method == 'POST':
        guia = usr
        name = request.form['name']
        ponto = request.form['ponto']
        data = request.form['data']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        lista = cursor.execute(
        '''
        SELECT * FROM passeios WHERE guia=? AND ponto=? AND data=?
        ''', (guia, ponto, data)
        ).fetchall()
        connection.commit()
        connection.close()
        id_passeio = lista[0][0]
        a = Passeio(tabela='passeios1', id_passeio=id_passeio, name_turista=name)
        validate = a.adicionar()
        if validate:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    if request.method == 'GET':
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

