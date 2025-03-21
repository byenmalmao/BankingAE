from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def index():
   return render_template('index.html')  # No incluyas 'templates/'

@app.route('/login')
def Login():
   return render_template('login.html')


@app.route('/registrar')
def Registrar():
   return render_template('registrar.html')

app.run(host="0.0.0.0", port=50100, debug=True)