from flask import Flask

app = Flask(__name__)

products = [
    {"id": 1, "name": "Product 1", "price": 10.99},
    {"id": 2, "name": "Product 2", "price": 19.99},
    {"id": 3, "name": "Product 3", "price": 5.99},
]

@app.route("/")
def home():
    return "Hello Flask"

@app.get("/products")
def list_products():
    return {"products": products}

@app.get("/products/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return {"product": product}, 200
    return {"error": "Product not found"}, 404

@app.post("/products")
def create_product():
    new_product = {"id": len(products) + 1, "name": "New Product", "price": 9.99}
    products.append(new_product)
    return {"message": "Product created", "product": new_product  }, 201




if __name__ == "__main__":
    app.run(debug=True)