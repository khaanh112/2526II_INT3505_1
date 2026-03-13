from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, make_response, request, g
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "change-thi  s-in-production"
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

products = [
    {"id": 1, "name": "Product 1", "price": 10.99},
    {"id": 2, "name": "Product 2", "price": 19.99},
    {"id": 3, "name": "Product 3", "price": 5.99},
]

USERS = {
    "mai": {"id": 1, "name": "Mai", "role": "user", "password": "123456"},
    "admin": {"id": 2, "name": "Admin", "role": "admin", "password": "admin456"},
}


def create_token(user):
    now = datetime.now(timezone.utc)
    exp = now + app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    payload = {
        "sub": str(user["id"]),
        "name": user["name"],
        "role": user["role"],
        "iat": now,
        "exp": exp,
    }
    return jwt.encode(
        payload,
        app.config["JWT_SECRET_KEY"],
        algorithm=app.config["JWT_ALGORITHM"],
    )


def decode_token(token):
    return jwt.decode(
        token,
        app.config["JWT_SECRET_KEY"],
        algorithms=[app.config["JWT_ALGORITHM"]],
    )

# Middleware
@app.before_request
def authenticate():
    public_paths = ["/", "/login"]

    if request.path in public_paths :
        return

    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = parts[1]
    try:
        claims = decode_token(token)
    except ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except InvalidTokenError:
        return jsonify({"error": "Invalid JWT token"}), 401

    user_id = claims.get("sub")
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid token subject"}), 401

    user = next((u for u in USERS.values() if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 401

    g.current_user = {"id": user["id"], "name": user["name"], "role": user["role"]}


@app.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        return {"error": "username and password are required"}, 400

    user = USERS.get(username)
    if not user or user["password"] != password:
        return {"error": "Invalid credentials"}, 401

    access_token = create_token(user)
    return {"access_token": access_token, "token_type": "Bearer"}, 200


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
    data = {"products": products,
            "links": {
                "self": "/products",
                "create": "/products",
                "product_detail": "/products/<id>",
                "update_product": "/products/<id>",
                "delete_product": "/products/<id>"
            }
            }
    response = make_response(jsonify(data))
    return response


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



@app.get("/code-on-demand")
def code_on_demand():
    
    python_code = """
products = {products}

def render_products(data):
    print("\\n[Code on Demand] Danh sách sản phẩm (rendered by code from server):")
    print("-" * 45)
    for p in data:
        print(f"  ID: {{p['id']}} | {{p['name']}} | ${{p['price']:.2f}}")
    print("-" * 45)
    print(f"Tổng: {{len(data)}} sản phẩm")

render_products(products)
""".format(products=products)

    return make_response(
        python_code,
        200,
        {"Content-Type": "text/x-python"}
    )


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "URL không tồn tại"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)