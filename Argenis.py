from flask import Flask 

app = Flask(__name__)
@app.route('/')

def puta():
    print("Eres puta?")
    respuesta = input("Responde si o no: ")
    if respuesta == "si":
        print ("OMG")
    else:
     print("lAstima")

@app.route('/hola')
def hola():
   print("MMG")