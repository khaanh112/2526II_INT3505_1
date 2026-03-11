from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Mai", "email": "mai@example.com"},
    {"id": 2, "name": "An", "email": "an@example.com"},
]

orders = [
    {"id": 1, "user_id": 1, "total": 100},
    {"id": 2, "user_id": 1, "total": 250},
    {"id": 3, "user_id": 2, "total": 180},
]


def success_response(data, message="Success", status_code=200):
    return jsonify({"success": True, "data": data, "message": message}), status_code


def error_response(code, message, status_code):
    return jsonify({"success": False, "error": {"code": code, "message": message}}), status_code


@app.get("/users")
def get_users():
    return success_response(users)

@app.get("/api/v1/users")
def get_users_v1():
    return success_response(users)


@app.get("/users/<int:user_id>")
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return error_response("USER_NOT_FOUND", "User not found", 404)
    return success_response(user)


@app.post("/users")
def create_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return error_response("VALIDATION_ERROR", "name and email are required", 400)

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(new_user)
    return success_response(new_user, "User created", 201)


@app.patch("/users/<int:user_id>")
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return error_response("USER_NOT_FOUND", "User not found", 404)

    data = request.get_json()
    if not data:
        return error_response("INVALID_BODY", "Request body is required", 400)

    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]

    return success_response(user, "User updated")


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return error_response("USER_NOT_FOUND", "User not found", 404)

    users = [u for u in users if u["id"] != user_id]
    return success_response(None, "User deleted")

@app.get("/users/<int:user_id>/orders")
def get_user_orders(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return error_response("USER_NOT_FOUND", "User not found", 404)
    user_orders = [o for o in orders if o["user_id"] == user_id]
    return success_response(user_orders)


@app.errorhandler(404)
def not_found(error):
    return error_response("NOT_FOUND", "URL không tồn tại", 404)


@app.errorhandler(405)
def method_not_allowed(error):
    return error_response("METHOD_NOT_ALLOWED", "HTTP method không được hỗ trợ", 405)


@app.errorhandler(500)
def internal_error(error):
    return error_response("INTERNAL_SERVER_ERROR", "Lỗi server nội bộ", 500)


if __name__ == "__main__":
    app.run(debug=True)