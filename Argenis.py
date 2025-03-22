from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from config import config
from flask_mysqldb import MySQL
from forms import LoginForm

from models.ModelUser import ModelUser

from models.entitties.User import User  

app = Flask(__name__)
db= MySQL(app)

app.config.from_pyfile('config.py')

# URL de la API gubernamental de validación de cédulas
API_VALIDACION_CEDULA = "https://api.digital.gob.do/validar-cedula"


@app.route('/')
def index():
    return redirect(url_for('login'))

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
         #print(request.form['username'])
         #print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password == True:
                return redirect(url_for('home'))
            else:
                flash('Contraseña incorrectos')
                return render_template('auth/login.html')
        else:
            flash('Usuario no encontrado')
            return render_template('auth/login.html')
     else:
         return render_template('auth/login.html')


# Página del formulario
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/Registrar')
def registrar():
    return render_template('registrar.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(host="0.0.0.0", port=50100, debug=True)