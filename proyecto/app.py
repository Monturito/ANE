from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

usuarios = [
    {'username': 'admin', 'password': 'admin'},
    {'username': 'usuario1', 'password': 'contrasena1'},
    {'username': 'usuario2', 'password': 'contrasena2'},
    {'username': 'usuario3', 'password': 'contrasena3'}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for usuario in usuarios:
            if username == usuario['username'] and password == usuario['password']:
                session['logged_in'] = True
                return redirect(url_for('store'))

        return render_template('index.html', error='Invalid credentials.')
    else:
        return render_template('index.html')
@app.route('/cart')
def show_cart():
    cart = session.get('cart', {})
    return jsonify(cart), 200

@app.route('/store')
def store():
    session.setdefault('cart', {})  # Inicializa session['cart'] con un diccionario vacío si no está presente

    if session.get('logged_in'): 
        cart = session['cart']

        nfts = [
            {
                'id': 1,
                'image_url': 'images/nft1.png',
                'price': 3500,
                'name': 'Edificio 1',
                'quantity': session['cart'].get(1, 0)
            },
            {
                'id': 2,
                'image_url': 'images/nft2.png',
                'price': 3500,
                'name': 'Edificio 2',
                'quantity': session['cart'].get(2, 0)
            },
            {
                'id': 3,
                'image_url': 'images/nft3.png',
                'price': 4500,
                'name': 'Edificio 3',
                'quantity': session['cart'].get(3, 0)
            },
            {
                'id': 4,
                'image_url': 'images/nft4.png',
                'price': 4500,
                'name': 'Edificio 4',
                'quantity': session['cart'].get(4, 0)
            },
            # ... Resto de los NFTs con precios ajustados
        ]

        return render_template('store.html', nfts=nfts, cart=session['cart'])
    else:
        return redirect(url_for('login'))
    


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()  # Obtener los datos enviados en la solicitud

    # Obtener productId y quantity de los datos recibidos
    productId = data.get('productId')
    quantity = data.get('quantity')

    # Realizar operaciones para agregar el producto al carrito
    # Aquí puedes agregar tu lógica para agregar el producto al carrito de acuerdo a tus necesidades
    cart = session.get('cart', {})
    cart[productId] = cart.get(productId, 0) + quantity
    session['cart'] = cart

    # Ejemplo de respuesta de éxito
    response = {
        'message': f'Product with ID {productId} added to cart successfully'
    }

    return jsonify(response), 200


@app.route('/comprar.html', methods=['GET', 'POST'])
def comprar():
    if session.get('logged_in'):
        cart = session.get('cart', {})

        nfts = [
            {
                'id': 1,
                'name': 'NFT 1',
                'price': 100,
                'quantity': 2
            },
            {
                'id': 2,
                'name': 'NFT 2',
                'price': 200,
                'quantity': 1
            }
            # ... otros datos de NFTs
        ]

        # Calcular el subtotal y el total de la compra
        subtotal = 0
        for nft_id, quantity in cart.items():
            for nft in nfts:
                if nft['id'] == nft_id:
                    subtotal += nft['price'] * quantity

        if request.method == 'POST':
            # Procesar el pago y realizar otras acciones necesarias
            session['cart'] = {}  # Limpiar el carrito después de la compra
            return render_template('confirmacion.html', subtotal=subtotal, total=subtotal)

        return render_template('comprar.html', cart=cart, nfts=nfts, subtotal=subtotal)
    else:
        return redirect(url_for('login'))

@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    # Puedes obtenerlos de una base de datos, de un archivo, o de cualquier otra fuente de datos
    product = {
        'id': product_id,
        'name': 'Oli',
        'price': 10.99,
        'description': 'Product Description'
    }

    return jsonify(product)


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    nft_id = request.json['nft_id']
    quantity = int(request.json['quantity'])

    if 'cart' in session:
        cart = session['cart']
        if nft_id in cart:
            cart[nft_id] = max(0, cart[nft_id] - quantity)
            if cart[nft_id] == 0:
                del cart[nft_id]

        session['cart'] = cart

    return 'Item removed from cart'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5003,debug=True)
