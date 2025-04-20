import sys
import os

# Agregar directorio de la carpeta static al sys.path para usar correctamente los métodos de db_actions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'static')))
print(sys.path)

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import pathlib
import requests
from pip._vendor import cachecontrol
from flask import Flask, abort, redirect, render_template, request, url_for, session, flash
import psycopg2
from db.db_actions import get_products, create_product, edit_product, delete_product
from db.connection import get_db_connection, close_db_connection

app = Flask(__name__)   

app.secret_key = "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"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOOGLE_CLIENT_ID = "846548093542-oip7o7ucj5a9ioopb8hfe5neufmqk4j1.apps.googleusercontent.com"
# Direccion del archivo client_secret.json
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, 'client_secret.json')

# Crear el flujo de autenticación de Google
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file, # Archivo de credenciales de Google
    scopes = ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"], # Permisos de acceso a la información del usuario
    redirect_uri="https://minimal-dvis.onrender.com/auth/google/callback" # URL de redirección después de la autenticación
)

#! FUNCIONES
# Funcion para verificar si el usuario inició sesión
def check_session():
    if 'google_id' in session:
        return True
    return False

#! RUTAS
#Rutas de autenticación con Google, para iniciar sesión
@app.route('/login_with_google')
def login_with_google():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

#Ruta de callback de Google, para recibir el token de autenticación
@app.route('/auth/google/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']:
        print(f"State mismatch: {session['state']} != {request.args['state']}")
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_request,
        audience=GOOOGLE_CLIENT_ID

    )
    session['google_id'] = id_info['sub']
    session['name'] = id_info['name']
    session['email'] = id_info['email']
    return redirect('/')

#Ruta para obtener la información del usuario autenticado
@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    # Verificar si el usuario inició sesión
    if 'google_id' in session:
        # Usuario autenticado con Google
        return {
            'isLoggedIn': True,
            'name': session.get('name', '')
        }
    else:
        # Usuario no autenticado
        return {
            'isLoggedIn': False
        }

#Ruta de la página principal
#Se verifica si el usuario ha iniciado sesión para mostrar la opción de cerrar sesión o iniciar sesión
@app.route('/')
def index():
    thereSession = check_session()
    return render_template('index.html', thereSession=thereSession)

#Ruta de la página de los productos
#Se verifica si el usuario ha iniciado sesión para mostrar la opción de cerrar sesión o iniciar sesión
#Se obtienen los productos de la base de datos
@app.route('/store')
def store():
    products = get_products()
    thereSession = check_session()
    return render_template('store.html',products=products, thereSession=thereSession)

#Ruta de la página de inicio de sesión
#Se obtienen los productos de la base de datos para hacer modificaciones, eliminarlos o crear nuevos
@app.route('/administrador')
def administrador():
    if 'logged_in' not in session:  
        return redirect(url_for('login'))
    products = get_products()
    return render_template('administrador.html', products=products)

#Ruta para el inicio de sesión del administrador
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '1234':
            session['logged_in'] = True
            return redirect(url_for('administrador'))
        else:
            error = 'Credenciales incorrectas. Por favor, intenta de nuevo.'
            return render_template('login.html', error=error)
        
    return render_template('login.html')

#Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#Ruta para agregar un producto
#Obtiene los datos del producto desde el formulario y los inserta en la base de datos para crear el nuevo producto
@app.route('/add_product', methods=['POST'])
def add_product_route():
    product_name = request.form.get('productName')
    product_price = request.form.get('productPrice')
    product_image = request.form.get('productImage')

    if product_name and product_price and product_image:
        create_product(product_price, product_image, product_name)
        return redirect(url_for('administrador'))
    else:
        return 'Error en el servidor', 400

#Ruta para editar un producto
#Obtiene los datos del producto desde el formulario y los actualiza en la base de datos
@app.route('/edit_product', methods=['POST'])
def edit_product_route():
    product_id = request.form.get('productID')
    product_name = request.form.get('productName')
    product_price = request.form.get('productPrice')
    product_image = request.form.get('productImage')

    # Si los datos están correctos, ejecuta la actualización
    if product_id and product_name and product_price and product_image:
        edit_product(product_id, product_price, product_image, product_name)
        return redirect(url_for('administrador'))
    else:
        return 'Error en el servidor', 400

#Ruta para eliminar un producto
#Obtiene el ID del producto desde el formulario y lo elimina de la base de datos
@app.route('/delete_product', methods=['POST'])
def delete_product_route():
    product_id = request.form.get('productID')
    
    # Si el ID del producto es correcto, ejecuta la eliminación
    if product_id:
        delete_product(product_id)
        return redirect(url_for('administrador'))
    else:
        return 'Error en el servidor', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)