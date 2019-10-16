from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/registrar')
def registrar():
    return render_template('registro.html')


if __name__ == '__main__':
    app.run(debug=True)
