from flask import Flask, request, jsonify, make_response
from functools import wraps
import datetime

app = Flask(__name__)

# --- MOCK DATABASE ---
users_db = [
    {"id": 1, "name": "Mai Khả Anh", "email": "khaanh@example.com"},
    {"id": 2, "name": "Nguyễn Văn B", "email": "b@example.com"}
]

# --- UTILS & DECORATORS ---

def deprecated(sunset_date, message):
    """
    Decorator để đánh dấu API đã lỗi thời.
    Thêm header Warning và thông tin ngày đóng cửa (Sunset).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            # Header Warning (chuẩn RFC 7234)
            response.headers['Warning'] = f'299 - "Deprecation: {message}"'
            # Header Sunset để client biết ngày API sẽ chính thức "nghỉ hưu"
            response.headers['Link'] = f'<{sunset_date}>; rel="sunset"'
            return response
        return decorated_function
    return decorator

# --- VERSIONING IMPLEMENTATIONS ---

# 1. URL Versioning: /api/v1/users (Legacy)
@app.route('/api/v1/users', methods=['GET'])
@deprecated("2026-12-31", "V1 is deprecated. Use V2 for separate first/last name fields.")
def get_users_v1():
    return jsonify({
        "version": "v1",
        "status": "deprecated",
        "data": users_db # Trả về field 'name' nguyên bản
    })

# 1. URL Versioning: /api/v2/users (New - Breaking Change)
@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    # Giả lập logic xử lý breaking change: tách tên
    data_v2 = []
    for user in users_db:
        name_parts = user['name'].split(' ')
        data_v2.append({
            "id": user['id'],
            "first_name": " ".join(name_parts[1:]),
            "last_name": name_parts[0],
            "email": user['email']
        })
    return jsonify({
        "version": "v2",
        "status": "active",
        "data": data_v2
    })

# 2. Query Parameter Versioning: /api/users?v=2
@app.route('/api/query/users', methods=['GET'])
def get_users_query():
    version = request.args.get('v', '1')
    if version == '2':
        return get_users_v2()
    return get_users_v1()

# 3. Header Versioning: X-API-Version: 2
@app.route('/api/header/users', methods=['GET'])
def get_users_header():
    version = request.headers.get('X-API-Version', '1')
    if version == '2':
        return get_users_v2()
    return get_users_v1()

# --- ERROR HANDLING ---

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error="Endpoint không tồn tại. Hãy kiểm tra lại version API."), 404

if __name__ == '__main__':
    # Flask v1 style: Chạy server ở cổng 5000
    app.run(host='0.0.0.0', port=5000, debug=True)