from app.static.db.connection import get_db_connection, close_db_connection
import psycopg2

#Funcion para obtener los productos de la base de datos
#Devuelve una lista de diccionarios con los productos
def get_products(): 
    conn, cur = get_db_connection()
    
    cur.execute('SELECT id, name, "imageURL", price FROM products')
    products = cur.fetchall()
    close_db_connection(conn, cur)

    # Devuelve una lista de diccionarios con los productos que se usará en las páginas para mostrarlos
    return [{"id": row[0], "name":row[1], "imageURL":row[2], "price": row[3]} for row in products] 


#Funcion para crear y agregar un nuevo producto a la base de datos
def create_product(price, imageURL, name):
    conn, cur = get_db_connection()
    cur.execute('INSERT INTO products (price, "imageURL", name) VALUES (%s, %s, %s)', (price, imageURL, name))
    conn.commit()
    close_db_connection(conn, cur)

#Funcion para borrar un producto de la base de datos
def delete_product(product_id):
    conn, cur = get_db_connection()
    cur.execute('DELETE FROM products WHERE id = %s', (product_id,))
    conn.commit()
    close_db_connection(conn, cur)

#Funcion para editar un producto de la base de datos
def edit_product(product_id, price, imageURL, name):
    conn, cur = get_db_connection()
    cur.execute('UPDATE products SET price = %s, "imageURL" = %s, name = %s WHERE id = %s', (price, imageURL, name, product_id))
    conn.commit()
    close_db_connection(conn, cur)
