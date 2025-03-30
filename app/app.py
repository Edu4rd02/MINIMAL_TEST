import sys
import os

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

app = Flask(__name__)   

app.secret_key = "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"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOOGLE_CLIENT_ID = "196038969225-eebje5m13p7c9qfut5sh3qi241kqp6hr.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, 'client_secret.json')

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes = ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_uri="https://minimal-dvis.onrender.com/auth/google/callback"
)

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'google_id' not in session:  
            return abort(401)
        else:
            return f()
    return wrapper

@app.route('/login_with_google')
def login_with_google():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

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
    print(f"User {session['name']} logged in with Google.")
    return redirect('/')


@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    # Verificar si el usuario está autenticado con Google o como admin
    if 'google_id' in session:
        # Usuario autenticado con Google
        return {
            'isLoggedIn': True,
            'name': session.get('name', ''),
            'email': session.get('email', ''),
            'authType': 'google'
        }
    else:
        # Usuario no autenticado
        return {
            'isLoggedIn': False
        }


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store')
def store():
    products = get_products()
    return render_template('store.html',products=products)

@app.route('/administrador')
def administrador():
    if 'logged_in' not in session:  
        return redirect(url_for('login'))
    products = get_products()
    return render_template('administrador.html', products=products)

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/add_product', methods=['POST'])
def add_product_route():
    product_name = request.form.get('productName')
    product_price = request.form.get('productPrice')
    product_image = request.form.get('productImage')

    # Si los datos están correctos, ejecuta la inserción
    if product_name and product_price and product_image:
        create_product(product_price, product_image, product_name)
        return redirect(url_for('administrador'))
    else:
        return 'Error en el servidor', 400

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
    app.run(debug=True)