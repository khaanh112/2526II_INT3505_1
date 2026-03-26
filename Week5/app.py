from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# --- Mock Data ---
products = [
    {"id": "p1", "name": "Smartphone X", "price": 999.0, "category_id": "c1", "stock": 50},
    {"id": "p2", "name": "Laptop Pro", "price": 1999.0, "category_id": "c1", "stock": 20},
    {"id": "p3", "name": "Wireless Headphones", "price": 199.0, "category_id": "c1", "stock": 100},
    {"id": "p4", "name": "Action Figure", "price": 49.0, "category_id": "c2", "stock": 30},
]

categories = [
    {"id": "c1", "name": "Electronics"},
    {"id": "c2", "name": "Toys"},
]

users = {
    "u1": {"id": "u1", "name": "Khoa Anh", "email": "khoaanh@example.com"},
}

carts = {
    "u1": {"items": [{"product_id": "p1", "quantity": 1}], "total": 999.0}
}

orders = {
    "u1": []
}

# --- Products Endpoints ---

@app.route('/v1/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    if category:
        filtered = [p for p in products if p['category_id'] == category]
        return jsonify(filtered)
    return jsonify(products)

@app.route('/v1/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        abort(404, description="Product not found")
    return jsonify(product)

# --- Categories Endpoints ---

@app.route('/v1/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)

@app.route('/v1/categories/<category_id>/products', methods=['GET'])
def get_category_products(category_id):
    filtered = [p for p in products if p['category_id'] == category_id]
    return jsonify(filtered)

# --- Users & Orders Endpoints ---

@app.route('/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user)

@app.route('/v1/users/<user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    user_orders = orders.get(user_id, [])
    return jsonify(user_orders)

@app.route('/v1/users/<user_id>/orders', methods=['POST'])
def place_order(user_id):
    cart = carts.get(user_id)
    if not cart or not cart['items']:
        abort(400, description="Cart is empty")
    
    new_order = {
        "order_id": f"ord_{len(orders.get(user_id, [])) + 1}",
        "status": "pending",
        "items": cart['items'],
        "total": cart['total']
    }
    orders.setdefault(user_id, []).append(new_order)
    carts[user_id] = {"items": [], "total": 0.0}  # Clear cart
    return jsonify(new_order), 201

# --- Cart Endpoints ---

@app.route('/v1/users/<user_id>/cart', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {"items": [], "total": 0.0})
    return jsonify(cart)

@app.route('/v1/users/<user_id>/cart/items', methods=['POST'])
def add_to_cart(user_id):
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        abort(404, description="Product not found")
    
    user_cart = carts.setdefault(user_id, {"items": [], "total": 0.0})
    user_cart['items'].append({"product_id": product_id, "quantity": quantity})
    user_cart['total'] += product['price'] * quantity
    
    return jsonify(user_cart), 200

# --- Error Handlers ---

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
