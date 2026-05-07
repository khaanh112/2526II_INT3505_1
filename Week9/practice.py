from flask import Flask, request, jsonify, make_response
from functools import wraps

app = Flask(__name__)

# Giả lập database
users_db = [
    {"id": 1, "name": "Mai Kha Anh", "email": "khaanh@example.com"},
    {"id": 2, "name": "Nguyễn Văn B", "email": "b@example.com"}
]

# --- UTILS & DECORATORS ---

def deprecated(sunset_date, message):
    """Decorator để chèn Header cảnh báo cho các API cũ"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            # Header Warning theo chuẩn RFC 7234
            response.headers['Warning'] = f'299 - "Deprecation: {message}"'
            # Header thông báo ngày chính thức tắt API
            response.headers['X-Sunset-Date'] = sunset_date
            return response
        return decorated_function
    return decorator

# --- API ENDPOINTS ---

# Chiến lược 1: URL Versioning - v1 (Legacy)
@app.route('/api/v1/users', methods=['GET'])
@deprecated("2026-12-31", "Phien ban v1 se ngung ho tro vao cuoi nam 2026. Hay chuyen sang v2.")
def get_users_v1():
    # V1 trả về nguyên bản field 'name'
    return jsonify({
        "version": "v1",
        "status": "deprecated",
        "data": users_db
    })

# Chiến lược 1: URL Versioning - v2 (Breaking Change)
@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    # Xử lý breaking change: Tách 'name' thành 'first_name' và 'last_name'
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

# Chiến lược 2: Query Parameter Versioning (/api/query/users?v=2)
@app.route('/api/query/users', methods=['GET'])
def get_users_query():
    version = request.args.get('v', '1')
    return get_users_v2() if version == '2' else get_users_v1()

# Chiến lược 3: Header Versioning (X-API-Version: 2)
@app.route('/api/header/users', methods=['GET'])
def get_users_header():
    version = request.headers.get('X-API-Version', '1')
    return get_users_v2() if version == '2' else get_users_v1()

# --- ERROR HANDLING ---

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found", "message": "Kiem tra lai version API"}), 404

if __name__ == '__main__':
    # Chạy debug mode để tự reload khi sửa code
    app.run(host='0.0.0.0', port=5000, debug=True)