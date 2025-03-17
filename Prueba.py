from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Usuario de prueba
USUARIO = {'username': 'admin', 'password': '1234', 'balance': 1000}

@app.route('/')
def home():
    if 'username' in session:
        return f"Bienvenido, {session['username']}! <a href='/logout'>Cerrar sesión</a> <br><a href='/account'>Cuenta bancaria</a>"
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USUARIO['username'] and password == USUARIO['password']:
            session['username'] = username
            session['balance'] = USUARIO['balance']
            return redirect(url_for('home'))
        return "Usuario o contraseña incorrectos. <a href='/login'>Intentar de nuevo</a>"
    return '''
        <form method='post'>
            Usuario: <input type='text' name='username'><br>
            Contraseña: <input type='password' name='password'><br>
            <input type='submit' value='Iniciar sesión'>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('balance', None)
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        action = request.form['action']
        amount = float(request.form['amount'])
        if action == 'deposit':
            session['balance'] += amount
        elif action == 'withdraw':
            if amount <= session['balance']:
                session['balance'] -= amount
            else:
                return "Saldo insuficiente. <a href='/account'>Volver</a>"
    return f"""Saldo actual: ${session['balance']} <br><br>
        <form method='post'>
            Monto: <input type='number' name='amount' step='0.01'><br>
            <button type='submit' name='action' value='deposit'>Depositar</button>
            <button type='submit' name='action' value='withdraw'>Retirar</button>
        </form>
        <br><a href='/'>Volver al inicio</a>"""

if __name__ == '__main__':
    app.run(debug=True)
