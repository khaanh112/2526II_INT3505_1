from pathlib import Path

from flask import Flask, Response, jsonify, request, send_file

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Fluent Python", "author": "Luciano Ramalho"},
]


def success_response(data=None, message="Success", status_code=200):
    return jsonify({"success": True, "message": message, "data": data}), status_code


def error_response(message, status_code=400):
    return jsonify({"success": False, "error": message}), status_code


def find_book(book_id):
    return next((book for book in books if book["id"] == book_id), None)


@app.get("/")
def index():
    return success_response(
        {
            "name": "Library API (Simple Demo)",
            "endpoints": [
                "GET /health",
                "GET /books",
                "GET /books/<book_id>",
                "POST /books",
                "PUT /books/<book_id>",
                "DELETE /books/<book_id>",
                "GET /docs",
            ],
        },
        "Library API is running",
    )


@app.get("/health")
def health():
    return success_response({"status": "ok"}, "Service healthy")


@app.get("/docs")
def docs_index():
        return success_response(
                {
                        "swagger_ui": "/docs/swagger",
                        "openapi": "/docs/openapi.yaml",
                        "api_blueprint": "/docs/api.apib",
                        "raml": "/docs/api.raml",
                        "typespec": "/docs/main.tsp",
                },
                "API docs endpoints",
        )


@app.get("/docs/openapi.yaml")
def docs_openapi():
        return send_file(BASE_DIR / "openapi" / "openapi.yaml", mimetype="application/yaml")


@app.get("/docs/api.apib")
def docs_api_blueprint():
        return send_file(BASE_DIR / "api-blueprint" / "api.apib", mimetype="text/plain")


@app.get("/docs/api.raml")
def docs_raml():
        return send_file(BASE_DIR / "raml" / "api.raml", mimetype="application/raml+yaml")


@app.get("/docs/main.tsp")
def docs_typespec():
        return send_file(BASE_DIR / "typesec" / "main.tsp", mimetype="text/plain")


@app.get("/docs/swagger")
def docs_swagger_ui():
        html = """
<!doctype html>
<html>
    <head>
        <meta charset=\"utf-8\" />
        <title>Library API Docs</title>
        <link rel=\"stylesheet\" href=\"https://unpkg.com/swagger-ui-dist@5/swagger-ui.css\" />
    </head>
    <body>
        <div id=\"swagger-ui\"></div>
        <script src=\"https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js\"></script>
        <script>
            window.ui = SwaggerUIBundle({
                url: '/docs/openapi.yaml',
                dom_id: '#swagger-ui'
            });
        </script>
    </body>
</html>
"""
        return Response(html, mimetype="text/html")


@app.get("/books")
def list_books():
    return success_response(books)


@app.get("/books/<int:book_id>")
def get_book(book_id):
    book = find_book(book_id)
    if not book:
        return error_response("Book not found", 404)
    return success_response(book)


@app.post("/books")
def create_book():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")
    author = payload.get("author")

    if not title or not author:
        return error_response("title and author are required", 400)

    new_book = {
        "id": (max([book["id"] for book in books]) + 1) if books else 1,
        "title": title,
        "author": author,
    }
    books.append(new_book)
    return success_response(new_book, "Book created", 201)


@app.put("/books/<int:book_id>")
def update_book(book_id):
    book = find_book(book_id)
    if not book:
        return error_response("Book not found", 404)

    payload = request.get_json(silent=True) or {}
    title = payload.get("title", book["title"])
    author = payload.get("author", book["author"])

    book["title"] = title
    book["author"] = author

    return success_response(book, "Book updated")


@app.delete("/books/<int:book_id>")
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return error_response("Book not found", 404)

    books.remove(book)
    return success_response(None, "Book deleted")


@app.errorhandler(404)
def not_found(_error):
    return error_response("Endpoint not found", 404)


@app.errorhandler(405)
def method_not_allowed(_error):
    return error_response("Method not allowed", 405)


if __name__ == "__main__":
    app.run(debug=True)
