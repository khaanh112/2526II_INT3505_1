import time
from flask import Flask, jsonify, request, abort
from pymongo import MongoClient, ASCENDING

app = Flask(__name__)

# --- MongoDB Setup ---
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client.get_database("week5_benchmark_db")
products_col = db.get_collection("products")

print("Checking MongoDB integration and database seed status...")
try:
    count = products_col.count_documents({})
    if count < 1000000:
        print(f"Current count {count} is less than 1,000,000. Seeding database...")
        products_col.delete_many({})
        batch = []
        # Seed 1M records in batches of 100,000
        for i in range(1, 1000001):
            batch.append({
                "_id": i,  # Using integer ID for efficient indexing and cursor pagination
                "id": f"p{i}", 
                "name": f"Product {i}", 
                "price": 10.0 * i, 
                "category_id": "c1" if i % 2 == 0 else "c2", 
                "stock": 100
            })
            if len(batch) >= 100000:
                products_col.insert_many(batch)
                batch = []
                print(f"Seeded {i} records...")
        if batch:
            products_col.insert_many(batch)
        print("Database seeding completed.")
    else:
        print("Database already contains 1,000,000 records. Skipping seed.")
        
    # Ensure Index on category_id for filtering
    products_col.create_index([("category_id", ASCENDING)])
except Exception as e:
    print(f"MongoDB connection error: {str(e)}")

# --- Mock Data for simple entities ---
categories = [
    {"id": "c1", "name": "Electronics"},
    {"id": "c2", "name": "Home & Garden"},
]

users = {
    "u1": {"id": "u1", "name": "Khoa Anh", "email": "khoaanh@example.com"},
}

carts = {"u1": {"items": [], "total": 0.0}}
orders = {"u1": []}

def format_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# --- Products Endpoints with NATIVE MongoDB Pagination ---
@app.route('/v1/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    
    # Base query for MongoDB
    query = {}
    if category:
        query['category_id'] = category
        
    total = products_col.count_documents(query)
    
    # 2. Pagination Parameters
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=None, type=int)
    page = request.args.get('page', default=None, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    after_id = request.args.get('after_id', default=None, type=str)
    
    # --- Strategy A: Cursor-based Pagination ---
    if after_id:
        # Expected after_id looks like "p100", extract the integer part "100"
        try:
            # Simple parsing since we seeded integer ids mapping to pXXX
            last_id = int(after_id.replace('p', ''))
            query['_id'] = {'$gt': last_id}
        except:
            pass
            
        cursor = products_col.find(query).sort('_id', ASCENDING).limit(limit)
        paginated_data = [format_doc(doc) for doc in cursor]
        
        next_cursor = paginated_data[-1]['id'] if len(paginated_data) == limit else None
        
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
        
        # MongoDB native skip/limit
        cursor = products_col.find(query).sort('_id', ASCENDING).skip(start).limit(per_page)
        paginated_data = [format_doc(doc) for doc in cursor]
        
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
        
    cursor = products_col.find(query).sort('_id', ASCENDING).skip(offset).limit(limit)
    paginated_data = [format_doc(doc) for doc in cursor]
    
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
    query = {"id": product_id}
    product = products_col.find_one(query)
    if not product:
        abort(404, description="Product not found")
    return jsonify(format_doc(product))

# --- Categories Endpoints ---
@app.route('/v1/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)

@app.route('/v1/categories/<category_id>/products', methods=['GET'])
def get_category_products(category_id):
    cursor = products_col.find({"category_id": category_id}).limit(100) # Safety limit
    return jsonify([format_doc(doc) for doc in cursor])

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
    carts[user_id] = {"items": [], "total": 0.0}
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
    
    product = products_col.find_one({"id": product_id})
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
