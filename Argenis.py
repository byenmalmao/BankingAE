from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, g, session
from config import config
from flask_mysqldb import MySQL
from forms import LoginForm
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_login import  LoginManager,login_user,login_required,logout_user
from flask_login import current_user 
from datetime import datetime, timedelta
from generarcuenta import generar_cuenta_fidebank

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
    logout_user()  # Limpia la autenticación de Flask-Login
    session.clear()  # Elimina todos los datos de sesión
    return redirect(url_for('login'))  # Redirige al login

@app.route('/protected')
@login_required
def protected():
    return 'Protected'

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return '404'

# Página del formulario
@login_required
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
        
        banco = 1  # ID del banco por defecto (puedes cambiarlo según tu lógica)
        saldo = 0.0  # Saldo inicial
        tipo = 'Ahorro'  # Tipo de cuenta por defecto
        fecha_apertura = datetime.now().strftime('%Y-%m-%d')  # Fecha y hora actual
        Numero_de_Cuenta= generar_cuenta_fidebank()
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
            
            cursor.execute(
                """INSERT INTO CUENTA
                (TipoCuenta, Saldo, FechaApertura, IdCliente, IdBanco, Numero_de_Cuenta) VALUES (%s,%s,%s,%s,%s,%s) """,
                (tipo, saldo, fecha_apertura, IdCliente,banco, Numero_de_Cuenta)
            )
            
            db.connection.commit()

            flash(f'Usuario: {username} \n- Contraseña: {password}', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.connection.rollback()
            
            error_str = str(e).lower()
            print(f"Error: {error_str}")  # Para depuración, puedes imprimir el error en la consola
            
           
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


# Ruta para ver todas las cuentas registradas
@app.route('/cuentas')
@login_required
def cuentas():
    
    # The accounts are already loaded in current_user.cuentas
    return render_template('cuentas.html', cuentas=current_user.cuenta)

def saldo_total(id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT COALESCE(SUM(Saldo), 0) FROM cuenta WHERE IdCliente = %s", (id,))
    total_saldo = cursor.fetchone()[0]  # Obtener el resultado de la consulta
    cursor.close()
    
    return total_saldo  # Devuelve un número en lugar de un string



@app.route('/solicitar_producto', methods=['GET', 'POST'])
def solicitar_producto():
    if request.method == 'POST':
        #Aqui se validaran los datos para ser insertados en la base de datos.
        
    # Obtener el ID del cliente de current_user
        if not hasattr(current_user, 'cliente'):
            return jsonify({"error": "Usuario no tiene cliente asociado"}), 400
        
        idcliente = current_user.cliente['IdCliente']
        print(f"DEBUG: IdCliente a insertar: {idcliente}")  # Verifica en consola
        
        idcliente = int(idcliente)  # Convertir a entero # ID del cliente (puedes obtenerlo de la sesión o de otra manera)
        #idcliente = request.form['idcliente']  # ID del cliente (puedes obtenerlo de la sesión o de otra manera)
        #idcliente = 1  # ID del cliente por defecto (puedes cambiarlo según tu lógica)
        # Obtener los datos del formulario
        tipo = str(request.form['tipocuenta'])  # Asegurar que sea string
        saldo = float(request.form['monto'])  # Convertir a número decimal
        descripcion = request.form.get('Descripcion', '').strip()  # Evitar None
        fecha_apertura = datetime.now().strftime('%Y-%m-%d')  # Fecha actual
        banco = 1  # ID del banco por defecto
        Numero_de_Cuenta= generar_cuenta_fidebank()
        
        cursor = db.connection.cursor()
        print(f"Intentando insertar cuenta para el cliente {idcliente}")
        cursor.execute(
            """INSERT INTO CUENTA
            (TipoCuenta, Saldo, FechaApertura, IdCliente, IdBanco, Numero_de_Cuenta, descripccion) VALUES (%s,%s,%s,%s,%s,%s,%s) """,
            (tipo, saldo, fecha_apertura, idcliente,banco, Numero_de_Cuenta, descripcion)
        )
        db.connection.commit()
        print(f"Cuenta creada con éxito: {tipo} con saldo {saldo} y número de cuenta {Numero_de_Cuenta} para el cliente {idcliente}")
        cursor.close()
        
        return jsonify({"success": f" Nueva cuenta creada: {Numero_de_Cuenta}"})
        
    return render_template('accounts/solicitar_producto.html')


@app.route('/detalle_cuenta', methods=['POST', 'GET'])
@login_required
def detalle_cuenta():
    
    numero = request.args.get('numero')
    cuenta = obtener_cuenta_por_id(numero)
    return render_template('accounts/detalle_cuenta.html', cuenta=cuenta)


def obtener_cuenta_por_id(numero):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM cuenta WHERE Numero_de_Cuenta = %s", (numero,))
    row = cursor.fetchone()
    cursor.close()
    
    if row:
        columnas = ["IdCuenta", "IdCliente", "IdBanco", "TipoCuenta", "Saldo", "FechaApertura", "Estado", "Numero_de_Cuenta", "Descripccion"]
        cuenta = dict(zip(columnas, row))
        return cuenta
    
    return None

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

@app.route('/transferir', methods=['GET', 'POST'])
@login_required
def transferir():
    if request.method == 'POST':
        try:
            cuenta_origen = request.form['cuenta_origen']
            cuenta_destino = request.form['cuenta_destino']
            monto = float(request.form['monto'])
            descripcion = request.form.get('descripcion', 'Transferencia')

            cur = db.connection.cursor()

            # 1. Obtener IdCliente del usuario actual
            cur.execute("""
                SELECT IdCliente FROM cliente 
                WHERE IdUsuario = %s
            """, (current_user.id,))
            cliente = cur.fetchone()
            
            if not cliente:
                flash('Cliente no encontrado', 'error')
                return redirect(url_for('transferir'))
                
            id_cliente = cliente[0]

            # 2. Verificar cuenta origen (pertenece al cliente)
            cur.execute("""
                SELECT IdCuenta, Saldo 
                FROM cuenta 
                WHERE Numero_de_Cuenta = %s AND IdCliente = %s
            """, (cuenta_origen, id_cliente))
            origen = cur.fetchone()

            if not origen:
                flash('Cuenta origen no válida', 'error')
                return redirect(url_for('transferir'))

            id_origen, saldo = origen

            # 3. Verificar cuenta destino (solo que exista)
            cur.execute("""
                SELECT IdCuenta 
                FROM cuenta 
                WHERE Numero_de_Cuenta = %s
            """, (cuenta_destino,))
            destino = cur.fetchone()

            if not destino:
                flash('Cuenta destino no existe', 'error')
                return redirect(url_for('transferir'))

            id_destino = destino[0]

            # Validaciones
            if id_origen == id_destino:
                flash('No puedes transferir a la misma cuenta', 'error')
                return redirect(url_for('transferir'))

            if saldo < monto:
                flash('Saldo insuficiente', 'error')
                return redirect(url_for('transferir'))

            # Realizar transferencia
            db.connection.begin()
            
            # Restar de origen
            cur.execute("""
                UPDATE cuenta 
                SET Saldo = Saldo - %s 
                WHERE IdCuenta = %s
            """, (monto, id_origen))
            
            # Sumar a destino
            cur.execute("""
                UPDATE cuenta 
                SET Saldo = Saldo + %s 
                WHERE IdCuenta = %s
            """, (monto, id_destino))
            
            # Registrar transacción
            cur.execute("""
                INSERT INTO transaccion (
                    IdCuentaOrigen, IdCuentaDestino, TipoTransaccion, 
                    Monto, FechaHora, Descripcion
                ) VALUES (%s, %s, 'Transferencia', %s, NOW(), %s)
            """, (id_origen, id_destino, monto, descripcion))
            
            db.connection.commit()
            flash('Transferencia exitosa', 'success')
            return redirect(url_for('transferir'))

        except Exception as e:
            db.connection.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('transferir'))
        finally:
            cur.close()

    # GET: Mostrar formulario
    cur = db.connection.cursor()
    
    # Obtener IdCliente primero
    cur.execute("SELECT IdCliente FROM cliente WHERE IdUsuario = %s", (current_user.id,))
    cliente = cur.fetchone()
    
    if not cliente:
        flash('Cliente no encontrado', 'error')
        return redirect(url_for('home'))
    
    # Obtener cuentas del cliente
    cur.execute("""
        SELECT Numero_de_Cuenta 
        FROM cuenta 
        WHERE IdCliente = %s AND Estado = 'Activa'
    """, (cliente[0],))
    cuentas = [row[0] for row in cur.fetchall()]
    cur.close()

    return render_template('transferir.html', cuentas=cuentas)

@app.route('/depositar', methods=['GET', 'POST'])
def depositar():
    if request.method == 'POST':
        numero_cuenta = request.form['numero_cuenta']
        monto = float(request.form['monto'])

        cursor = db.connection.cursor()

        # Verificar si la cuenta existe
        cursor.execute("SELECT IdCuenta FROM cuenta WHERE Numero_de_Cuenta = %s", (numero_cuenta,))
        cuenta = cursor.fetchone()

        if not cuenta:
            flash('Número de cuenta no válido', 'error')
            return redirect(url_for('depositar'))

        id_cuenta = cuenta[0]

        # Realizar el depósito
        try:
            cursor.execute("UPDATE cuenta SET Saldo = Saldo + %s WHERE IdCuenta = %s", (monto, id_cuenta))
            
            # Registrar la transacción
            cursor.execute("""
                INSERT INTO transaccion (IdCuentaOrigen, TipoTransaccion, Monto, FechaHora, Descripcion) 
                VALUES (%s, 'Depósito', %s, %s, %s)
            """, (id_cuenta, monto, datetime.now(), "Depósito realizado"))
            
            db.connection.commit()
            flash('Depósito realizado con éxito', 'success')
        except Exception as e:
            db.connection.rollback()
            flash(f"Error en la transacción: {str(e)}", 'error')

        return redirect(url_for('depositar'))

    return render_template('depositar.html')
# Ruta para la seccion de contactanos.
@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')
@app.route('/actividad')
@login_required
def actividad():
    # Inicializar variables esenciales
    transacciones = []
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total = 0
    tipos = []
    
    try:
        # Obtener parámetros de filtro
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        tipo_transaccion = request.args.get('tipo', 'Todas')

        # Obtener conexión a la base de datos
        cur = db.connection.cursor()
        
        # 1. Obtener ID del cliente
        cur.execute("""
            SELECT c.IdCliente 
            FROM cliente c
            JOIN usuario u ON c.IdUsuario = u.IdUsuario
            WHERE u.IdUsuario = %s
        """, (current_user.id,))
        cliente = cur.fetchone()

        if not cliente:
            flash('Cliente no encontrado', 'error')
            return redirect(url_for('home'))

        id_cliente = cliente[0]

        # 2. Construir consulta base
        query = """
            SELECT 
                t.IdTransaccion,
                t.FechaHora,
                t.TipoTransaccion,
                t.Monto,
                t.Descripcion,
                co.Numero_de_Cuenta AS CuentaOrigen,
                cd.Numero_de_Cuenta AS CuentaDestino
            FROM transaccion t
            LEFT JOIN cuenta co ON t.IdCuentaOrigen = co.IdCuenta
            LEFT JOIN cuenta cd ON t.IdCuentaDestino = cd.IdCuenta
            WHERE (co.IdCliente = %s OR cd.IdCliente = %s)
        """
        params = [id_cliente, id_cliente]

        # 3. Aplicar filtros
        if fecha_inicio:
            query += " AND t.FechaHora >= %s"
            params.append(fecha_inicio)
        
        if fecha_fin:
            query += " AND t.FechaHora <= %s"
            params.append(f"{fecha_fin} 23:59:59")
        
        if tipo_transaccion != 'Todas':
            query += " AND t.TipoTransaccion = %s"
            params.append(tipo_transaccion)

        # 4. Contar total de registros
        count_query = f"SELECT COUNT(*) FROM ({query}) AS subquery"
        cur.execute(count_query, params)
        total = cur.fetchone()[0]

        # 5. Obtener datos paginados
        data_query = query + " ORDER BY t.FechaHora DESC LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])
        cur.execute(data_query, params)
        transacciones = cur.fetchall()

        # 6. Obtener tipos de transacción disponibles
        cur.execute("""
            SELECT DISTINCT TipoTransaccion 
            FROM transaccion t
            JOIN cuenta c ON t.IdCuentaOrigen = c.IdCuenta OR t.IdCuentaDestino = c.IdCuenta
            WHERE c.IdCliente = %s
        """, (id_cliente,))
        tipos = ['Todas'] + [row[0] for row in cur.fetchall()]

        # 7. Configurar fechas por defecto
        fecha_fin_default = datetime.now().strftime('%Y-%m-%d')
        fecha_inicio_default = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    except Exception as e:
        flash(f'Error al obtener actividad: {str(e)}', 'error')
        return redirect(url_for('home'))
    
    finally:
        if 'cur' in locals():
            cur.close()

    # 8. Renderizar plantilla (fuera del try-except para garantizar el return)
    return render_template(
        'actividad.html',
        transacciones=transacciones,
        page=page,
        per_page=per_page,
        total=total,
        tipos=tipos,
        tipo_seleccionado=tipo_transaccion,
        fecha_inicio=fecha_inicio if fecha_inicio else fecha_inicio_default,
        fecha_fin=fecha_fin if fecha_fin else fecha_fin_default,
        request_args=request.args
    )
##################################################################################

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(host="0.0.0.0", port=50100, debug=True)