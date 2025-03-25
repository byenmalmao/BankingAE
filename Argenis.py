from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, g
from config import config
from flask_mysqldb import MySQL
from forms import LoginForm
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_login import  LoginManager,login_user,login_required,logout_user

from models.ModelUser import ModelUser

from models.entitties.User import User  

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'     #Recordar cambiar con sus datos 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tdohmgrj'
app.config['MYSQL_DB'] = 'fidebank'

app.secret_key = 'mysecretkey'

db= MySQL(app)

csrf=CSRFProtect(app)

# Cerrar la conexión a la base de datos después de cada solicitud
@app.teardown_appcontext
def teardown_db(exception):
    if hasattr(g, 'db'):
        g.db.close()

login_manager = LoginManager(app)

app.config.from_pyfile('config.py')

@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


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
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Contraseña incorrectos')
                return render_template('auth/login.html')
        else:
            flash('Usuario no encontrado')
            return render_template('auth/login.html')
     else:
         return render_template('auth/login.html')

#Log Out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return 'Protected'

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return '404'

# Página del formulario
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/Perfil')
def perfil():
    return  redirect('index.php')

import random
import hashlib  # Para encriptar la contraseña

@app.route('/registrar', methods=['GET', 'POST'])  #Argenis
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        documento = request.form['documento']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        estado = request.form['estado']

        # Generar una contraseña aleatoria de 6 dígitos
        password_numerica = str(random.randint(100000, 999999))

        # Encriptar la contraseña antes de guardarla
        password_encriptada = generate_password_hash(password_numerica)

        cursor = db.connection.cursor()

        try:
            # Insertar nuevo cliente
            cursor.execute("""
                INSERT INTO cliente (Nombre, Apellido, DocumentoIdentidad, Correo, Telefono, Direccion, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, documento, correo, telefono, direccion, estado))
            
            db.connection.commit()

            # Obtener el último ID insertado (IdCliente)
            cliente_id = cursor.lastrowid

            # Insertar usuario con el mismo nombre y la contraseña generada
            cursor.execute("""
                INSERT INTO usuario (username, password)
                VALUES (%s, %s)
            """, (nombre, password_encriptada))

            db.connection.commit()

            flash(f'Usuario creado: {nombre} - Contraseña: {password_numerica}', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.connection.rollback()
            flash(f'Error al registrar cliente: {str(e)}', 'error')

        finally:
            cursor.close()

    return render_template('registrar.html')




##################################################################################
# Ruta para crear un nuevo usuario
@app.route('/create_user', methods=['GET', 'POST'])  #Se crea automatico Argenis Cambios . 
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        amount = request.form['amount']

        db = db()
        cursor = db.cursor()

        # Verificar si el email ya existe
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('Email Already Exist !! Please use another Email', 'error')
        else:
            # Insertar nuevo usuario
            cursor.execute("INSERT INTO users (name, email, amount) VALUES (%s, %s, %s)", (name, email, amount))
            db.commit()
            flash('Congrats!! New User added', 'success')
            return redirect(url_for('index'))

    return render_template('create_user.html')

# Ruta para ver todos los usuarios
@app.route('/all_users')
def all_users():
    db = db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('all_users.html', users=users)

# Ruta para transferir dinero
@app.route('/transfer_money', methods=['GET', 'POST'])
def transfer_money():
    if request.method == 'POST':
        from_id = request.form['from_id']
        to_id = request.form['to_id']
        amount = float(request.form['amount'])

        db = db()
        cursor = db.cursor(dictionary=True)

        # Obtener información del remitente y receptor
        cursor.execute("SELECT * FROM users WHERE id = %s", (from_id,))
        sender = cursor.fetchone()
        cursor.execute("SELECT * FROM users WHERE id = %s", (to_id,))
        receiver = cursor.fetchone()

        if amount < 0:
            flash('Oops! Negative values cannot be Transferred', 'error')
        elif amount > sender['amount']:
            flash('Oops! Insufficient Amount', 'error')
        elif amount == 0:
            flash('Oops! Zero value cannot be Transferred', 'error')
        else:
            # Actualizar saldos
            new_sender_amount = sender['amount'] - amount
            new_receiver_amount = receiver['amount'] + amount

            cursor.execute("UPDATE users SET amount = %s WHERE id = %s", (new_sender_amount, from_id))
            cursor.execute("UPDATE users SET amount = %s WHERE id = %s", (new_receiver_amount, to_id))

            # Registrar la transacción
            cursor.execute("INSERT INTO transaction (sender, receiver, amount) VALUES (%s, %s, %s)",
                           (sender['name'], receiver['name'], amount))
            db.commit()

            flash('Transaction Successful', 'success')
            return redirect(url_for('index'))

    db = db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('transfer_money.html', users=users)

# Ruta para ver el historial de transacciones
@app.route('/transfer_log')
def transfer_log():
    db = db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transaction")
    transactions = cursor.fetchall()
    return render_template('transfer_log.html', transactions=transactions)

# Ruta para contactar
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        db = db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO contact (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                       (name, email, subject, message))
        db.commit()

        flash('Message Sent Successfully', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')
##################################################################################

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(host="0.0.0.0", port=50100, debug=True)