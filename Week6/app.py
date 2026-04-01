from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# Secret key
JWT_SECRET = 'super_secret_jwt_key_week_6'
PORT = 3000

# Dummy users database
users = [
    { "id": 1, "username": 'admin', "password": 'password123', "role": 'admin' },
    { "id": 2, "username": 'user1', "password": 'user123', "role": 'user' }
]

# 2. Middleware để xác thực và giải mã JWT Token
def authenticate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"message": "Không có quyền truy cập. Token bị thiếu."}), 401
        
        token = auth_header.split(' ')[1]
        
        try:
            # Xác thực token
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            # Lưu thông tin giải mã vào request.user và đi tiếp
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token không hợp lệ hoặc đã hết hạn."}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token không hợp lệ hoặc đã hết hạn."}), 403
            
        return f(*args, **kwargs)
    return decorated

# 1. Chức năng Đăng nhập (Login) -> Trả về JWT Token
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Tài khoản hoặc mật khẩu không đúng"}), 401
    
    username = data.get('username')
    password = data.get('password')
    
    # Kiểm tra thông tin người dùng
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    
    if not user:
        return jsonify({"message": "Tài khoản hoặc mật khẩu không đúng"}), 401
        
    # Tạo payload chứa thông tin người dùng
    payload = {
        "userId": user['id'],
        "username": user['username'],
        "role": user['role'],
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    
    # Ký token (Sign token) với secret key, hạn sử dụng là 1 giờ
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    # Trả JWT token về cho client
    return jsonify({
        "message": "Đăng nhập thành công",
        "token": token
    })

# 3. API được bảo vệ (Chỉ người có Token mới gọi được)
@app.route('/api/profile', methods=['GET'])
@authenticate_token
def profile():
    return jsonify({
        "message": "Truy cập thông tin người dùng thành công!",
        "user": request.user # Thông tin user được lấy từ token
    })

# 4. API được phân quyền (Chỉ admin mới gọi được)
@app.route('/api/admin', methods=['GET'])
@authenticate_token
def admin():
    if request.user.get('role') != 'admin':
        return jsonify({"message": "Từ chối truy cập. Yêu cầu quyền admin."}), 403
        
    return jsonify({
        "message": "Chào mừng truy cập trang quản trị hệ thống admin.",
        "user": request.user
    })

if __name__ == '__main__':
    print(f"Server JWT API đang chạy tại http://localhost:{PORT}")
    app.run(port=PORT, debug=True)
