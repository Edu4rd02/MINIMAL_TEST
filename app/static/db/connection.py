import psycopg2

#Funcion para crear la conexión a la base de datos
#La base de datos es PostgreSQL y se encuentra en linea en render.com
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

#Funcion para cerrar la conexión a la base de datos
#Cierra el cursor y la conexión a la base de datos
def close_db_connection(conn, cur): 
    try:
        if cur:
            cur.close()
        if conn:
            conn.close()
    except Exception as e:
        print("Error al cerrar la conexión:", e)