from flask import Flask

app = Flask(__name__)
@app.route('/')

def Hola():
    print("Hola")c