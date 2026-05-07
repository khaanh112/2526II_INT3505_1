from flask import Flask, jsonify

app = Flask(__name__)

# Giả lập database
users_db = [
    {"id": 1, "name": "Mai Kha Anh", "email": "khaanh@example.com"},
    {"id": 2, "name": "Nguyen Van B", "email": "b@example.com"}
]

# URL VERSIONING: Version 1
@app.route('/api/v1/users', methods=['GET'])
def get_users_v1():
    return jsonify({
        "version": "v1",
        "data": users_db
    })



@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    data_v2 = []
    for user in users_db:
        names = user['name'].split(' ')
        data_v2.append({
            "id": user['id'],
            "first_name": " ".join(names[1:]),
            "last_name": names[0],
            "email": user['email']
        })
    return jsonify({
        "version": "v2",
        "status": "active",
        "data": data_v2
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)