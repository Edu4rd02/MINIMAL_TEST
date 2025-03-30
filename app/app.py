import sys
import os

# Agrega 'static' a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'static')))

from flask import Flask, redirect, render_template, request, url_for, session, flash
import psycopg2
from static.db.db_actions import get_products, create_product, edit_product, delete_product

app = Flask(__name__)
app.secret_key = 'clave_secreta_minimal'

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
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/add_product', methods=['POST'])
def add_product_route():
    product_name = request.form.get('productName')
    product_price = request.form.get('productPrice')
    product_image = request.form.get('productImage')

    # Si los datos están correctos, ejecuta la inserción
    if product_name and product_price and product_image:
        create_product(product_price, product_image, product_name)
        products = get_products()
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