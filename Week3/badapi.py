from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Mai", "email": "mai@example.com"},
    {"id": 2, "name": "An", "email": "an@example.com"},
]


@app.get("/getUsers")
def getUsers():
    return jsonify(users)


@app.post("/deleteUser")
def deleteUser():
    user_id = request.args.get("id")
    return jsonify({"message": f"user {user_id} deleted"})


@app.get("/UserDetails/<int:id>")
def UserDetails(id):
    user = next((u for u in users if u["id"] == id), None)
    if not user:
        return jsonify({"msg": "not found"})
    return jsonify(user)


@app.post("/createNewUser")
def createNewUser():
    data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "name": data.get("name"),
        "email": data.get("email")
    }
    users.append(new_user)
    return jsonify({"status": "ok", "data": new_user})


if __name__ == "__main__":
    app.run(debug=True)