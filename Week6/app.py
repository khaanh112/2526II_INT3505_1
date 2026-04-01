from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# Hai Secret key riêng biệt cho an toàn bảo mật
JWT_SECRET = 'super_secret_jwt_key_week_6'
REFRESH_SECRET = 'another_super_secret_refresh_key' 
PORT = 3000

# Dummy users database (Đã bổ sung Roles và Scopes cho từng user)
users = [
    { 
        "id": 1, 
        "username": 'admin', 
        "password": 'password123', 
        "role": 'admin',
        "scopes": ['read:profile', 'write:data', 'delete:user'] # Scopes của Admin 
    },
    { 
        "id": 2, 
        "username": 'user1', 
        "password": 'user123', 
        "role": 'user',
        "scopes": ['read:profile'] # Sinh viên/User thường chỉ có tính năng đọc
    }
]

# ----------------------------------------------------
# MIDDLEWARES
# ----------------------------------------------------

# 1. Xác thực Bearer Token
def authenticate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Lấy token từ header Authorization theo format: Bearer <token>
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"message": "Không có quyền truy cập. Cần Bearer Token."}), 401
        
        token = auth_header.split(' ')[1]
        
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = decoded # Lưu thông tin user để dùng trong các Route phía dưới
        except jwt.ExpiredSignatureError:
            # Báo lỗi Access Token để Frontend biết đường vác Refresh Token đi gọi API /api/refresh
            return jsonify({"message": "Access Token đã hết hạn. Hãy dùng Refresh Token để lấy token mới."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token không hợp lệ."}), 403
            
        return f(*args, **kwargs)
    return decorated

# 2. Xác thực Phạm vi quyền (Scopes) 
def require_scope(required_scope):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_scopes = request.user.get('scopes', [])
            if required_scope not in user_scopes:
                return jsonify({"message": f"Thiếu quyền (Scope). Yêu cầu scope: '{required_scope}'"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

# ----------------------------------------------------
# ROUTES CỦA ỨNG DỤNG
# ----------------------------------------------------

# [1] API Đăng nhập -> Trả về Access Token & Refresh Token
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Thiếu thông tin"}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    
    if not user:
        return jsonify({"message": "Tài khoản hoặc mật khẩu sai"}), 401
        
    # Tạo Access Token (Thời gian sống RẤT NGẮN - 15 phút chẳng hạn)
    access_payload = {
        "userId": user['id'],
        "username": user['username'],
        "role": user['role'],
        "scopes": user['scopes'],
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
    }
    access_token = jwt.encode(access_payload, JWT_SECRET, algorithm="HS256")
    
    # Tạo Refresh Token (Thời gian sống LÂU - 7 ngày)
    refresh_payload = {
        "userId": user['id'],
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }
    refresh_token = jwt.encode(refresh_payload, REFRESH_SECRET, algorithm="HS256")
    
    return jsonify({
        "message": "Đăng nhập thành công",
        "access_token": access_token,   # Sẽ gửi trong header API call
        "refresh_token": refresh_token  # Cất kĩ, chỉ để xin lại access_token
    })

# [2] API Cấp lại Access Token mới (khi token cũ hết hạn)
@app.route('/api/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({"message": "Không tìm thấy Refresh Token"}), 400
        
    try:
        # Giải mã Refresh Token bằng SECRET riêng biệt
        decoded = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])
        user_id = decoded['userId']
        
        # Tìm lại User hiện tại trong DB
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return jsonify({"message": "Người dùng không tồn tại"}), 404
            
        # Cấp lại Access Token mới tinh (sống thêm 15 phút nữa)
        access_payload = {
            "userId": user['id'],
            "username": user['username'],
            "role": user['role'],
            "scopes": user['scopes'],
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
        }
        new_access_token = jwt.encode(access_payload, JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            "message": "Đã làm mới Access Token thành công",
            "access_token": new_access_token
        })
        
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh Token đã hết hạn. Bắt buộc đăng nhập lại."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Refresh Token bị lỗi."}), 403


# [3] Yêu cầu Access Token Hợp Lệ (Bất kỳ user nào login xong)
@app.route('/api/profile', methods=['GET'])
@authenticate_token
def profile():
    return jsonify({
        "message": "Đọc thông tin cá nhân. Nhận Bearer Token thành công",
        "user": request.user
    })

# [4] Phân quyền bằng ROLE (Dành cho admin)
@app.route('/api/admin', methods=['GET'])
@authenticate_token
def admin():
    if request.user.get('role') != 'admin':
        return jsonify({"message": "ROLE Từ chối: Bạn không phải Admin!"}), 403
        
    return jsonify({
        "message": "Bạn đang login là Admin. Vượt qua cửa ải kiểm tra ROLES thành công.",
        "user": request.user
    })

# [5] Phân quyền bằng SCOPE cụ thể
@app.route('/api/write_data', methods=['POST'])
@authenticate_token # 1. Bắt buộc phải có Bearer Token đã
@require_scope('write:data') # 2. Bắt buộc Token phải mang SCOPE 'write:data'
def write_data():
    return jsonify({
        "message": "Token của bạn có chứa Scope 'write:data'. Đã thực hiện thao tác tạo dữ liệu mới thành công!"
    })

if __name__ == '__main__':
    print(f"Server Đóng vai trò Demo JWT (Có Scopes, Roles, Refresh Token) API đang chạy tại http://localhost:{PORT}")
    app.run(port=PORT, debug=True)
