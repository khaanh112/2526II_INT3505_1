from flask import Flask, current_app, jsonify, make_response, request, g

app = Flask(__name__)

products = [
    {"id": 1, "name": "Product 1", "price": 10.99},
    {"id": 2, "name": "Product 2", "price": 19.99},
    {"id": 3, "name": "Product 3", "price": 5.99},
]

TOKENS = {
    "token_user_123": {"id": 1, "name": "Mai", "role": "user"},
    "token_admin_456": {"id": 2, "name": "Admin", "role": "admin"},
}

# Middleware: chạy trước mỗi request
@app.before_request
def authenticate():
    # Những route public không cần token
    public_paths = ["/", "/products"]
    is_product_detail = request.path.startswith("/products/") and request.method == "GET"

    if request.path in public_paths or is_product_detail:
        return

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401

    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({"error": "Invalid Authorization format"}), 401

    token = parts[1]
    user = TOKENS.get(token)

    if not user:
        return jsonify({"error": "Invalid token"}), 401

    g.current_user = user  # Lưu thông tin user vào context toàn cục


@app.route("/")
def home():
    return "Hello Flask"

@app.get("/profile")
def profile():
    user = getattr(g, "current_user", None)
    if user:
        return {"profile": user}, 200
    return {"error": "Unauthorized"}, 401


@app.get("/products")
def list_products():
    return {"products": products,
            "links": {
                "self": "/products",
                "create": "/products",
                "product_detail": "/products/<id>",
                "update_product": "/products/<id>",
                "delete_product": "/products/<id>"
            }
            }, 200

@app.get("/products/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        data = {"product": product,
                "links": {
                    "self": f"/products/{product_id}",
                    "update": f"/products/{product_id}",
                    "delete": f"/products/{product_id}"
                }
        }
        response = make_response(jsonify(data))
        response.headers["Cache-Control"] = "public, max-age=3600"  
        return response
    return {"error": "Product not found"}, 404

@app.post("/products")
def create_product():
    new_product = {"id": len(products) + 1, "name": "New Product", "price": 9.99}
    products.append(new_product)
    return {"message": "Product created", "product": new_product  }, 201


@app.put("/products/<int:product_id>")
def update_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        product["name"] = "Updated Product"
        product["price"] = 14.99
        return {"message": "Product updated", "product": product}, 200
    return {"error": "Product not found"}, 404


@app.delete("/products/<int:product_id>")
def delete_product(product_id):
    delete_product = next((p for p in products if p["id"] == product_id), None)
    if delete_product:
        products.remove(delete_product)
        return {"message": "Product deleted"}, 200
    return {"error": "Product not found"}, 404



@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "URL không tồn tại"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)