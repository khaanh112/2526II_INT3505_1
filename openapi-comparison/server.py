from datetime import datetime
from pathlib import Path

from flask import Flask, Response, jsonify, request, send_file

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "year": 2008,
        "available": True,
    },
    {
        "id": 2,
        "title": "Fluent Python",
        "author": "Luciano Ramalho",
        "year": 2015,
        "available": True,
    },
]

members = [
    {"id": 1, "name": "Nguyen An", "email": "an.nguyen@example.com"},
    {"id": 2, "name": "Tran Binh", "email": "binh.tran@example.com"},
]

borrow_records = []


def success_response(data=None, message="Success", status_code=200):
    return jsonify({"success": True, "message": message, "data": data}), status_code


def error_response(message, status_code=400):
    return jsonify({"success": False, "error": message}), status_code


def find_book(book_id):
    return next((book for book in books if book["id"] == book_id), None)


def find_member(member_id):
    return next((member for member in members if member["id"] == member_id), None)


@app.get("/")
def index():
    return success_response(
        {
            "name": "Library Management Demo",
            "endpoints": [
                "GET /books",
                "GET /books/<book_id>",
                "POST /books",
                "PUT /books/<book_id>",
                "DELETE /books/<book_id>",
                "GET /members",
                "POST /borrow",
                "POST /return",
                "GET /borrow-records",
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
    keyword = request.args.get("q", "").strip().lower()
    available = request.args.get("available")

    result = books

    if keyword:
        result = [
            book
            for book in result
            if keyword in book["title"].lower() or keyword in book["author"].lower()
        ]

    if available in {"true", "false"}:
        expected = available == "true"
        result = [book for book in result if book["available"] == expected]

    return success_response(result)


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
    year = payload.get("year")

    if not title or not author or not isinstance(year, int):
        return error_response("title, author and year(int) are required", 400)

    new_book = {
        "id": (max([book["id"] for book in books]) + 1) if books else 1,
        "title": title,
        "author": author,
        "year": year,
        "available": True,
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
    year = payload.get("year", book["year"])

    if not isinstance(year, int):
        return error_response("year must be int", 400)

    book["title"] = title
    book["author"] = author
    book["year"] = year

    return success_response(book, "Book updated")


@app.delete("/books/<int:book_id>")
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return error_response("Book not found", 404)

    if not book["available"]:
        return error_response("Cannot delete borrowed book", 409)

    books.remove(book)
    return success_response(None, "Book deleted")


@app.get("/members")
def list_members():
    return success_response(members)


@app.post("/borrow")
def borrow_book():
    payload = request.get_json(silent=True) or {}
    book_id = payload.get("book_id")
    member_id = payload.get("member_id")

    if not isinstance(book_id, int) or not isinstance(member_id, int):
        return error_response("book_id and member_id must be int", 400)

    book = find_book(book_id)
    if not book:
        return error_response("Book not found", 404)

    member = find_member(member_id)
    if not member:
        return error_response("Member not found", 404)

    if not book["available"]:
        return error_response("Book is already borrowed", 409)

    record = {
        "book_id": book_id,
        "member_id": member_id,
        "borrowed_at": datetime.utcnow().isoformat() + "Z",
        "returned_at": None,
    }
    borrow_records.append(record)
    book["available"] = False

    return success_response(record, "Borrow successful", 201)


@app.post("/return")
def return_book():
    payload = request.get_json(silent=True) or {}
    book_id = payload.get("book_id")

    if not isinstance(book_id, int):
        return error_response("book_id must be int", 400)

    book = find_book(book_id)
    if not book:
        return error_response("Book not found", 404)

    if book["available"]:
        return error_response("Book is not borrowed", 409)

    active_record = next(
        (
            record
            for record in reversed(borrow_records)
            if record["book_id"] == book_id and record["returned_at"] is None
        ),
        None,
    )

    if not active_record:
        return error_response("Active borrow record not found", 404)

    active_record["returned_at"] = datetime.utcnow().isoformat() + "Z"
    book["available"] = True

    return success_response(active_record, "Return successful")


@app.get("/borrow-records")
def list_borrow_records():
    return success_response(borrow_records)


@app.errorhandler(404)
def not_found(_error):
    return error_response("Endpoint not found", 404)


@app.errorhandler(405)
def method_not_allowed(_error):
    return error_response("Method not allowed", 405)


if __name__ == "__main__":
    app.run(debug=True)
