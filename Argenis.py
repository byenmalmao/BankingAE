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
app.config['MYSQL_PASSWORD'] = 'Bismuto888@#'
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
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        
        if logged_user is not None:
            if logged_user.password:  # Si la contraseña es correcta
                login_user(logged_user)
                
                # Ejemplo: Acceder a datos del cliente
                if logged_user.cliente:
                    print(f"Cliente: {logged_user.cliente['Nombre']}")
                
                return redirect(url_for('home'))
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Usuario no encontrado', 'error')
    
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
        username = request.form['username']
        password = request.form['password']
        # Validar que el correo no esté ya registrado
        
        # Generar una contraseña aleatoria de 6 dígitos
       # password_numerica = str(random.randint(100000, 999999))

        # Encriptar la contraseña antes de guardarla
        password_encriptada = generate_password_hash(password)

        cursor = db.connection.cursor()

        try:
            # 1. Primero insertar el USUARIO (para obtener su ID)
            cursor.execute(
                "INSERT INTO usuario (username, password) VALUES (%s, %s)",
                (username, password_encriptada)
            )
            IdUsuario = cursor.lastrowid  # Obtenemos el ID del usuario recién creado
            db.connection.commit()

            # 2. Insertar el CLIENTE con el user_id
            cursor.execute(
                """INSERT INTO cliente 
                (Nombre, Apellido, DocumentoIdentidad, Correo, Telefono, Direccion, Estado, IdUsuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (nombre, apellido, documento, correo, telefono, direccion, estado, IdUsuario)
            )
            IdCliente= cursor.lastrowid  # ID del cliente recién creado
            db.connection.commit()

            # 3. Actualizar el USUARIO con el cliente_id
            cursor.execute(
                "UPDATE usuario SET IdCliente= %s WHERE IdUsuario = %s",
                (IdCliente, IdUsuario)
            )
            db.connection.commit()

            flash(f'Usuario: {username} \n- Contraseña: {password}', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.connection.rollback()
            
            # Identificar el campo duplicado
            error_msg = "Error al registrar. Por favor intente nuevamente."
            error_str = str(e).lower()
            
            if 'username' in error_str:
                error_msg = f"El nombre de usuario '{username}' ya está en uso"
            elif 'correo' in error_str:
                error_msg = f"El correo '{correo}' ya está registrado"
            elif 'documentoidentidad' in error_str:
                error_msg = "El número de documento ya existe en el sistema"
            elif 'documento' in error_str:  # Por si acaso
                error_msg = "El número de documento ya existe en el sistema"
            
            flash(error_msg, 'error')
            return render_template('registrar.html', 
                                form_data=request.form)  # Para mantener los datos ingresados

        finally:
            cursor.close()

    return render_template('registrar.html')




##################################################################################
# Ruta para la página de actividad (transacciones realizadas)
@app.route('/actividad')
def actividad():
    return render_template('actividad.html')

# Ruta para ver todas las cuentas registradas
@app.route('/cuentas')
def cuentas():
    return render_template('cuentas.html')
# Ruta para acceder a la sección de tarjetas
@app.route('/tarjetas')
def tarjetas():
    return render_template('tarjetas.html')

# Ruta para la sección de soporte
@app.route('/acerca_de')
def acerca_de():
    return render_template('acerca_de.html')

# Ruta para realizar transferencias
@app.route('/About')
def About():
    return render_template('about.html')

# Ruta para realizar transferencias
@app.route('/transferir')
def transferir():
    return render_template('transferir.html')

# Ruta para la seccion de contactanos.
@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')

##################################################################################

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(host="0.0.0.0", port=50100, debug=True)