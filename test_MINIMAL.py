from flask import session
from requests import patch
from app.main import app, check_session
from app.static.db import db_actions
from app.static.db.connection import get_db_connection, close_db_connection
import pytest

#Configuramos un cliente para hacer pruebas en los endpoints de la aplicación en Flask
#Esto funciona para hacer peticiones o acciones en el servidor sin necesidad de abrir el navegador
@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

#!Tests para añadir un producto a la base de datos
#Esta función cuenta con 4 conjuntos de parámetros
@pytest.mark.parametrize("name, price, image", [
    ("Camisa Oversize", "19.99", "image.jpg"),
    ("Camisa Oversize", "-19.99", "image.jpg"),
    ("Camisa Oversize", "gasdfawe", "image.jpg"),
    ("Camisa Oversize", "19.99", "")
])
def test_create_product(client, name, price, image):

    # Datos que se enviarán al formulario por parte del cliente creado para la prueba
    #Estos datos van cambiando en base a los conjuntos de parametros definidos en el @pytest.mark.parametrize
    data = {
        "productName": name,
        "productPrice": price,
        "productImage": image
    }

    # Realiza el POST al endpoint '/add_product'
    response = client.post("/add_product", data=data, content_type='application/x-www-form-urlencoded')

    # Confirma que el programa haya hecho una redirección (código 302)
    assert response.status_code == 302

#!Tests para editar un producto en la base de datos
#Esta funcion cuenta con 2 conjuntos de parametros
@pytest.mark.parametrize("name, price, image", [
    ("Pantalon Oversize", "19.99", ""),
    ("Pantalon Oversize", "-19.99", "image.jpg"),
    ("Pantalon Oversize", "1.5123412412", "image.jpg"),
    ("Pantalon Oversize", "19.99", "image.jpg")
])
def test_edit_product(client, name, price, image):
    # Se obtiene el ID del producto que se va a editar en la base de datos.
    # Esto no sería necesario si el proceso se realizará directamente desde el sitio web
    conn,cur = get_db_connection()
    cur.execute("SELECT id FROM products where name = %s",("Camisa Oversize",))
    result = cur.fetchall()

    # Datos que se enviarán al formulario por parte del cliente creado para la prueba
    #Estos datos van cambiando en base a los conjuntos de parametros definidos en el @pytest.mark.parametrize
    data = {
        "productID": result[0][0],
        "productName": name,
        "productPrice": price,
        "productImage": image
    }

    response = client.post("/edit_product", data=data, content_type='application/x-www-form-urlencoded')
    assert response.status_code == 302  # 302 indica que hubo una redirección

#!Tests para eliminar un producto de la base de datos
# Se encarga de buscar el ID del producto que se va a eliminar 
# Al final comprueba que este haya sido eliminado correctamente
def test_delete_product_form(client):
    conn, cur = get_db_connection()
    cur.execute("SELECT id FROM products WHERE name = %s", ("Pantalon Oversize",))
    result = cur.fetchall()

    response = client.post("/delete_product", data={"productID": result[0][0]}, content_type='application/x-www-form-urlencoded')
    
    cur.execute("SELECT id FROM products WHERE name = %s", ("Pantalon Oversize",))

    result = cur.fetchall()
    assert len(result) is 0  # Verifica que el producto exista antes de eliminarlo

#!Tests para verificar la función check_session
# Esta función comprueba si la sesión contiene un 'google_id' válido.
# Si 'google_id' está presente en la sesión, la función debe devolver True.
# Si no está presente, la función debe devolver False.
def test_check_session():
    with app.test_request_context():
        # Verifica que la función devuelve True cuando 'google_id' está en la sesión
        session['google_id'] = '12345'
        assert check_session() is True

        # Verifica que la función devuelve False cuando 'google_id' no está en la sesión
        session.clear()
        assert check_session() is False


#! Tests para la autenticación con Google
def test_login_with_google_redirect(client):
    response = client.get('/login_with_google')
    assert response.status_code == 302
    assert 'accounts.google.com' in response.location

#!Tests para verificar la ruta index
def test_index_route(client):

    response = client.get('/')
    assert response.status_code == 200

    # Verifica que se está utilizando la plantilla index.html
    assert b'<!DOCTYPE html>' in response.data

#!Tests para verificar la ruta de la tienda
def test_store_route(client):

    response = client.get('/store')
    assert response.status_code == 200

    # Verifica que hay productos en la respuesta
    assert b'products' in response.data

#!Tests para verificar el inicio de sesión del administrador
@pytest.mark.parametrize("username, password, expected_status", [
    ("admin", "1234", 302),  # Credenciales correctas - debe redirigir
    ("admin", "incorrect", 200),  # Contraseña incorrecta - debe mostrar error
    ("not_admin", "1234", 200),  # Usuario incorrecto - debe mostrar error
    ("", "", 200)  # Campos vacíos - debe mostrar error
])
def test_admin_login(client, username, password, expected_status):
    data = {
        "username": username,
        "password": password
    }
    
    response = client.post("/login", data=data, content_type='application/x-www-form-urlencoded')
    assert response.status_code == expected_status
    
    if username == "admin" and password == "1234":
        assert response.location == "/administrador"
    else:
        assert b'Credenciales incorrectas' in response.data

#!Tests para verificar el cierre de sesión
def test_logout(client):
    # Simula una sesión iniciada
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['google_id'] = '12345'
    
    # Realiza el cierre de sesión
    response = client.get("/logout")
    
    # Verifica la redirección a la página principal
    assert response.status_code == 302
    assert response.location == "/"
    
    # Verifica que la sesión se haya borrado
    with client.session_transaction() as session:
        assert 'logged_in' not in session
        assert 'google_id' not in session

#!Tests para verificar la API de información del usuario
def test_get_user_info_api(client):
    # Prueba sin sesión iniciada
    response = client.get("/api/user-info")
    assert response.status_code == 200
    # Convierte la respuesta JSON a diccionario
    data = response.get_json()
    assert data['isLoggedIn'] is False
    
    # Prueba con sesión iniciada con Google
    with client.session_transaction() as session:
        session['google_id'] = '12345'
        session['name'] = 'Test User'
        session['email'] = 'test@example.com'
    
    response = client.get("/api/user-info")
    assert response.status_code == 200
    data = response.get_json()
    assert data['isLoggedIn'] is True
    assert data['name'] == 'Test User'
