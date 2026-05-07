from flask import Flask, jsonify
from flask import make_response
from functools import wraps

app = Flask(__name__)

# Giả lập database
users_db = [
    {"id": 1, "name": "Mai Kha Anh", "email": "khaanh@example.com"},
    {"id": 2, "name": "Nguyen Van B", "email": "b@example.com"}
]


def deprecated(message):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            response.headers['Warning'] = f'299 - "Deprecated API: {message}"'
            response.headers['X-API-Deprecation-Date'] = '2026-12-31'
            return response
        return decorated_function
    return decorator


@app.route('/api/v1/users', methods=['GET'])
@deprecated("V1 will be EOL by end of 2026. Please migrate to /api/v2/users")
def get_users_v1():
    return jsonify({
        "version": "v1",
        "status": "deprecated",
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