from static.db.connection import get_db_connection, close_db_connection
import psycopg2

def get_products():
    conn, cur = get_db_connection()
    
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    close_db_connection(conn, cur)

    return [{"id": row[0], "price": row[1], "imageURL":row[2], "name":row[3]} for row in products]


def create_product(price, imageURL, name):
    conn, cur = get_db_connection()
    cur.execute('INSERT INTO products (price, "imageURL", name) VALUES (%s, %s, %s)', (price, imageURL, name))
    conn.commit()
    close_db_connection(conn, cur)

def delete_product(product_id):
    conn, cur = get_db_connection()
    cur.execute('DELETE FROM products WHERE id = %s', (product_id,))
    conn.commit()
    close_db_connection(conn, cur)

def edit_product(product_id, price, imageURL, name):
    conn, cur = get_db_connection()
    cur.execute('UPDATE products SET price = %s, "imageURL" = %s, name = %s WHERE id = %s', (price, imageURL, name, product_id))
    conn.commit()
    close_db_connection(conn, cur)
