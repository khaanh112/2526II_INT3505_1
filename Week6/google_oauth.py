from flask import Flask, redirect, url_for, session, jsonify, render_template
from authlib.integrations.flask_client import OAuth
import os
import json
from dotenv import load_dotenv

# Load các biến môi trường từ file .env
load_dotenv()

app = Flask(__name__)

app.secret_key = 'google-oauth-secret-key-for-week6-demo'
app.config['SESSION_COOKIE_NAME'] = 'google-auth-session'
# Cho phép gửi cookie khi ở localhost qua HTTP
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ----------------------------------------------------
# Cấu hình Google OAuth
# ----------------------------------------------------

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=os.getenv('CLIENT_ID'), 
    client_secret=os.getenv('CLIENT_SECRET'),
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# ----------------------------------------------------
# ROUTES
# ----------------------------------------------------

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return render_template('profile.html', user=user, user_json=json.dumps(user, indent=4))
    return render_template('index.html')

@app.route('/login')
def login():
    # Tạo redirect URL tới Google
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth')
def auth():
    try:
        # Xử lý callback từ Google sau khi User đồng ý đăng nhập
        token = oauth.google.authorize_access_token()
        
        # Thử lấy userinfo từ ID Token trước
        user = token.get('userinfo')
        
        # Nếu chưa có user, ta gọi endpoint userinfo của Google (Fallback)
        if not user:
            resp = oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo')
            user = resp.json()
            
        if user:
            session['user'] = user
            print(f"--- ĐĂNG NHẬP THÀNH CÔNG: {user.get('email')} ---")
        return redirect('/')
    except Exception as e:
        print(f"--- LỖI ĐĂNG NHẬP: {str(e)} ---")
        return jsonify({
            "error_message": "Không thể đăng nhập bằng Google.",
            "details": str(e),
        }), 400

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    os.environ['AUTHLIB_INSECURE_TRANSPORT'] = 'true'
    print("\n" + "="*50)
    print("Google OAuth Demo server is starting on http://localhost:5000")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
