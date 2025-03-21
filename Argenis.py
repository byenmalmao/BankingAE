from flask import Flask, request, render_template, jsonify
import requests  # Importa la librería requests para hacer llamadas HTTP

app = Flask(__name__)

# URL de la API gubernamental de validación de cédulas
API_VALIDACION_CEDULA = "https://api.digital.gob.do/validar-cedula"

# Página del formulario
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el registro
@app.route('/registrar', methods=['POST'])
def registrar():
    cedula = request.form.get('cedula')

    if not cedula:
        return jsonify({"error": "Cédula es obligatoria"}), 400

    # Simulación de validación (Reemplaza esto con la API real)
    try:
        response = requests.get(f"{API_VALIDACION_CEDULA}/{cedula}")
        if response.status_code == 200:
            data = response.json()
            if data.get("valido"):
                return jsonify({
                    "mensaje": "Cédula válida",
                    "nombre": data.get("nombre")
                }), 200
            else:
                return jsonify({"error": "Cédula inválida"}), 400
        else:
            return jsonify({"error": "Error validando la cédula"}), 500
    except Exception as e:
        return jsonify({"error": f"Error en la conexión: {str(e)}"}), 500

# Ruta para la página de inicio
@app.route('/homee')
def indexx():
    return render_template('index.html')

# Ruta para la página de login
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=50100, debug=True)