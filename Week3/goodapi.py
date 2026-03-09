from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Mai", "email": "mai@example.com"},
    {"id": 2, "name": "An", "email": "an@example.com"},
]


@app.get("/users")
def get_users():
    return jsonify(users), 200


@app.get("/users/<int:user_id>")
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "USER_NOT_FOUND", "message": "User not found"}), 404
    return jsonify(user), 200


@app.post("/users")
def create_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({
            "error": "VALIDATION_ERROR",
            "message": "name and email are required"
        }), 400

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(new_user)
    return jsonify(new_user), 201


@app.patch("/users/<int:user_id>")
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "USER_NOT_FOUND", "message": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({
            "error": "INVALID_BODY",
            "message": "Request body is required"
        }), 400

    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]

    return jsonify(user), 200


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "USER_NOT_FOUND", "message": "User not found"}), 404

    users = [u for u in users if u["id"] != user_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)