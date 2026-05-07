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

if __name__ == '__main__':
    app.run(debug=True, port=5000)