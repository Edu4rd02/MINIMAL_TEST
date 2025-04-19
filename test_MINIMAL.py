from app.main import app
from app.static.db import db_actions
from app.static.db.connection import get_db_connection, close_db_connection
from google.oauth2 import id_token
import pytest

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     return app.test_client()

def test_obtener_productos():
    conn, cur = get_db_connection()
    usuarios = db_actions.get_products()
    assert "Jordan 1" in usuarios[2]['name'] # Verifica que el nombre del primer producto sea "2"

# def test_create_product(get_db_connection):
#     conn, cur = get_db_connection
#     try:
#         db_actions.create_product(price="19.99", imageURL="agua.jpg", name="Agua Mineral",conn=conn, cur=cur, autocommit=False)
        
#         # Verificación
#         cur.execute("SELECT * FROM products WHERE name = %s", ("Agua Mineral",))
#         result = cur.fetchone()
#         assert result is not None
#         assert result[2] == "Agua Mineral"
#     finally:
#         conn.rollback()  # Rollback manual
#     # El rollback se hará automáticamente al finalizar la prueba

# def test_add_product_form(client, get_db_connection):
#     # Datos para enviar en el formulario
#     data = {
#         "productName": "Agua Mineral",
#         "productPrice": "19.99",
#         "productImage": "agua.jpg"
#     }

#     # Realiza el POST al endpoint '/add_product'
#     response = client.post("/add_product", data=data, content_type='application/x-www-form-urlencoded')

#     # Verifica que la respuesta sea una redirección (código 302)
#     assert response.status_code == 302  # 302 indica que hubo una redirección
    
#     # Verifica que el producto fue insertado correctamente
#     conn, cur = get_db_connection  # Obtener la conexión y el cursor del fixture
#     cur.execute("SELECT * FROM products WHERE name = %s", ("Agua Mineral",))
#     result = cur.fetchone()

#     assert result is not None  # Verifica que el producto exista
#     assert result[2] == "Agua Mineral"  # Verifica que el nombre del producto sea el esperado
