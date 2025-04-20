from app.main import app
from app.static.db import db_actions
from app.static.db.connection import get_db_connection, close_db_connection
import pytest

#Configuramos un cliente para hacer pruebas en los endpoints de la aplicación en Flask
#Esto funciona para hacer peticiones o acciones en el servidor sin necesidad de abrir el navegador
@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_obtener_productos():
    conn, cur = get_db_connection()
    usuarios = db_actions.get_products()
    assert "Jordan 1" in usuarios[2]['name'] # Verifica que el nombre del primer producto sea "2"

#!Tests para añadir un producto a la base de datos
#Esta funcion cuenta con 2 conjuntos de parametros
@pytest.mark.parametrize("name, price, image", [
    ("Agua Mineral", "19.99", "image.jpg"),
    ("Agua Mineral", "-19.99", "image.jpg"),
    ("Agua Mineral", "gasdfawe", "image.jpg"),
    ("Agua Mineral", "19.99", "")
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
    ("Agua orga", "19.99", ""),
    ("Agua orga", "-19.99", "image.jpg"),
    ("Agua orga", "1.5123412412", "image.jpg"),
    ("Agua orga", "19.99", "image.jpg")
])
def test_edit_product(client, name, price, image):
    # Se obtiene el ID del producto que se va a editar en la base de datos.
    # Esto no sería necesario si el proceso se realizará directamente desde el sitio web
    conn,cur = get_db_connection()
    cur.execute("SELECT id FROM products where name = %s",("Agua Mineral",))
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
    cur.execute("SELECT id FROM products WHERE name = %s", ("Agua orga",))
    result = cur.fetchall()

    response = client.post("/delete_product", data={"productID": result[0][0]}, content_type='application/x-www-form-urlencoded')
    
    cur.execute("SELECT id FROM products WHERE name = %s", ("Agua orga",))

    result = cur.fetchall()
    assert len(result) is 0  # Verifica que el producto exista antes de eliminarlo
