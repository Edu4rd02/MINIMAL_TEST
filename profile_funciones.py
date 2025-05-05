from app.static.db.connection import close_db_connection
from decimal import *
from memory_profiler import profile
import psycopg2

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="minimalproducts",
            user="minimalproducts_user",
            password="16HLKUZiQVLO7Go2tlZ15OjdhZpJ5WlR",
            host="dpg-d09vb5qdbo4c73e5chvg-a.oregon-postgres.render.com",
            port="5432"
        )
        cur = conn.cursor() #Crea un cursor para ejecutar consultas
        return conn, cur # Devuelve la conexión y el cursor
    
    except Exception as e:
        print("Error al crear el cursor:", e)
        conn.close()
        return None

def get_db_connection_ref():
    try:
        conn = psycopg2.connect(
            dbname="minimalproducts",
            user="minimalproducts_user",
            password="16HLKUZiQVLO7Go2tlZ15OjdhZpJ5WlR",
            host="dpg-d09vb5qdbo4c73e5chvg-a.oregon-postgres.render.com",
            port="5432"
        )
        conn.autocommit = True # Se elimina ante la falta de transacciones en la base de datos
        cur = conn.cursor() #Crea un cursor para ejecutar consultas
        return conn, cur # Devuelve la conexión y el cursor
    
    except Exception as e:
        print("Error al crear el cursor:", e)
        conn.close()
        return None


#Funcion para obtener los productos de la base de datos
#Devuelve una lista de diccionarios con los productos
@profile
def get_products(): 
    conn, cur = get_db_connection()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    close_db_connection(conn, cur)

    # Devuelve una lista de diccionarios con los productos que se usará en las páginas para mostrarlos
    return [{"id": row[0], "price": row[1], "imageURL":row[2], "name":row[3]} for row in products] 

#Funcion para obtener los productos de la base de datos refactorizada
@profile
def get_products_ref(): 
    conn, cur = get_db_connection_ref()
    
    cur.execute('SELECT id, name, "imageURL", price FROM products')
    products = cur.fetchall()
    close_db_connection(conn, cur)

    # Devuelve una lista de diccionarios con los productos que se usará en las páginas para mostrarlos
    return [{"id": row[0], "name":row[1], "imageURL":row[2], "price": row[3]} for row in products] 

#Funcion para crear y agregar un nuevo producto a la base de datos
@profile
def create_product(price, imageURL, name):
    conn, cur = get_db_connection()
    cur.execute('INSERT INTO products (price, "imageURL", name) VALUES (%s, %s, %s)', (price, imageURL, name))
    conn.commit()
    close_db_connection(conn, cur)

#Funcion para crear y agregar un nuevo producto a la base de datos refactorizada
@profile
def create_product_ref(price, imageURL, name):
    conn, cur = get_db_connection_ref()
    cur.execute('INSERT INTO products (price, "imageURL", name) VALUES (%s, %s, %s)', (price, imageURL, name))
    close_db_connection(conn, cur)

#Funcion para editar un producto de la base de datos
@profile
def edit_product(product_id, price, imageURL, name):
    conn, cur = get_db_connection()
    cur.execute('UPDATE products SET price = %s, "imageURL" = %s, name = %s WHERE id = %s', (price, imageURL, name, product_id))
    conn.commit()
    close_db_connection(conn, cur)

#Funcion para editar un producto de la base de datos refactorizada
@profile
def edit_product_ref(product_id, price, imageURL, name):
    conn, cur = get_db_connection_ref()
    cur.execute('UPDATE products SET price = %s, "imageURL" = %s, name = %s WHERE id = %s', (price, imageURL, name, product_id))
    close_db_connection(conn, cur)

#Funcion para borrar un producto de la base de datos
@profile
def delete_product(product_id):
    conn, cur = get_db_connection()
    cur.execute('DELETE FROM products WHERE id = %s', (product_id,))
    conn.commit()
    close_db_connection(conn, cur)

#Funcion para borrar un producto de la base de datos refactorizada
@profile
def delete_product_ref(product_id):
    conn, cur = get_db_connection_ref()
    cur.execute('DELETE FROM products WHERE id = %s', (product_id,))
    close_db_connection(conn, cur)


# Funcion para verificar si el precio es correcto
# Se asegura que el precio sea mayor o igual a 1 y que tenga dos decimales como máximo
@profile
def price_format(price):
    try:
        price = Decimal(price)
        if price >= 1 and price.as_tuple().exponent >= -2:
            return True
        else:
            return False
    except (ValueError, InvalidOperation):
        return False

# Funcion para verificar si el precio es correcto refactorizada
@profile
def price_format_ref(price):
    try:
        price = float(price)
        return price >= 1 and round(price, 2) == price
    except (ValueError, TypeError):
        return False



def principal():
    products = get_products()
    products_ref = get_products_ref()
    create_product(10.99, 'https://example.com/image.jpg', 'Nuevo Producto')
    create_product_ref(10.99, 'https://example.com/image.jpg', 'Nuevo Producto Ref')
    edit_product(38, 15.99, 'https://example.com/image-edit.jpg', 'Producto Editado')
    edit_product_ref(39, 15.99, 'https://example.com/image-edit.jpg', 'Producto Editado Ref')
    delete_product(46)
    delete_product_ref(51)
    price_format(1499.99)
    price_format_ref(1499.99)

if __name__ == "__main__":
    principal()