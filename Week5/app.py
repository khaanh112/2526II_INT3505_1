from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# --- Mock Data ---
# Expanded products list for pagination (1,000,000 items)
products = [
    {"id": f"p{i}", "name": f"Product {i}", "price": 10.0 * i, "category_id": "c1" if i % 2 == 0 else "c2", "stock": 100}
    for i in range(1, 1000001)
]

# Simulate Database Index (Allows O(1) jump access instead of full table scan)
product_index_map = { p['id']: i for i, p in enumerate(products) }


categories = [
    {"id": "c1", "name": "Electronics"},
    {"id": "c2", "name": "Home & Garden"},
]

users = {
    "u1": {"id": "u1", "name": "Khoa Anh", "email": "khoaanh@example.com"},
}

carts = {
    "u1": {"items": [], "total": 0.0}
}

orders = {
    "u1": []
}

# --- Products Endpoints with Pagination ---

@app.route('/v1/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    data = products
    
    # 1. Filtering
    if category:
        data = [p for p in data if p['category_id'] == category]
    
    total = len(data)
    
    # 2. Pagination Parameters
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=None, type=int)
    page = request.args.get('page', default=None, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    after_id = request.args.get('after_id', default=None, type=str)
    
    # 3. Strategy Detection & Logic
    
    # --- Strategy A: Cursor-based Pagination ---
    if after_id:
        # Simulate Index Scan -> O(1) Jump directly
        # In case 'category' is filtered, normally DB index handles it but we just use map.
        start_index = 0
        
        # O(1) Dictionary Lookup simulates Database Index hits
        if not category:
            start_index = product_index_map.get(after_id, -1) + 1
        else:
            # Fallback if filtered, though real DB composite indexes fix this.
            for i, p in enumerate(data):
                if p['id'] == after_id:
                    start_index = i + 1
                    break
        
        paginated_data = data[start_index : start_index + limit]
        next_cursor = paginated_data[-1]['id'] if len(paginated_data) == limit and start_index + limit < total else None
        
        return jsonify({
            "items": paginated_data,
            "metadata": {
                "total": total,
                "count": len(paginated_data),
                "limit": limit,
                "next_cursor": next_cursor,
                "strategy": "cursor"
            }
        })
    
    # --- Strategy B: Page-based Pagination ---
    if page is not None:
        start = (page - 1) * per_page
        
        # Simulate Database Sequential Scan penalty for throwing away N offset rows
        for _ in range(start): 
            pass 
            
        end = start + per_page
        paginated_data = data[start:end]
        
        return jsonify({
            "items": paginated_data,
            "metadata": {
                "total": total,
                "count": len(paginated_data),
                "page": page,
                "per_page": per_page,
                "total_pages": (total + per_page - 1) // per_page,
                "strategy": "page-based"
            }
        })
    
    # --- Strategy C: Offset/Limit Pagination (Default) ---
    if offset is None:
        offset = 0
        
    # Simulate Database Sequential Scan penalty for throwing away N offset rows
    for _ in range(offset): 
        pass 
        
    paginated_data = data[offset : offset + limit]
    
    return jsonify({
        "items": paginated_data,
        "metadata": {
            "total": total,
            "count": len(paginated_data),
            "offset": offset,
            "limit": limit,
            "strategy": "offset-limit"
        }
    })

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
