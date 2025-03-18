from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/ay')
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

if __name__ == '__main__':
    app.run(debug = True)