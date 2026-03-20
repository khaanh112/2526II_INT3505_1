# INT3505 - Demo API theo tuần

Repository này chứa các bài thực hành theo từng tuần cho môn INT3505, tập trung vào:
- xây dựng API với Flask,
- so sánh thiết kế API chưa tốt vs tốt,
- tài liệu hoá API bằng OpenAPI/Swagger.

## Cấu trúc thư mục

```text
Week1/
Week2/
	client.py
	server.py
Week3/
	badapi.py
	goodapi.py
Week4/
	openapi.yaml
	requirements.txt
	server.py
```

## Yêu cầu môi trường

- Python 3.10+
- pip

## Week2 - Flask cơ bản + JWT + Code on Demand

### File chính
- `Week2/server.py`: API Flask có đăng nhập JWT, middleware xác thực, CRUD sản phẩm.
- `Week2/client.py`: client gọi endpoint `/code-on-demand` và thực thi code nhận về.

### Chạy local

```bash
cd Week2
pip install flask pyjwt requests
python server.py
```

Server mặc định chạy tại `http://127.0.0.1:5000`.

### Tài khoản mẫu
- User: `mai` / `123456`
- Admin: `admin` / `admin456`

## Week3 - So sánh API design

### File chính
- `Week3/badapi.py`: ví dụ API chưa tốt (naming không nhất quán, endpoint chưa RESTful).
- `Week3/goodapi.py`: ví dụ API tốt hơn (RESTful, chuẩn response, error handling rõ ràng, versioning).

### Chạy local

```bash
cd Week3
pip install flask
python badapi.py
# hoặc
python goodapi.py
```

## Week4 - Student Management API + OpenAPI

### File chính
- `Week4/server.py`: API quản lý sinh viên (`/students`, `/health`) + Swagger UI.
- `Week4/openapi.yaml`: đặc tả OpenAPI 3.0.3.
- `Week4/requirements.txt`: dependency cho Week4.

### Chạy local

```bash
cd Week4
pip install -r requirements.txt
python server.py
```

### URL quan trọng
- Live server: https://2526-ii-int-3505-1-theta.vercel.app/
- Swagger UI local: http://127.0.0.1:5000/docs
- OpenAPI local: http://127.0.0.1:5000/openapi.yaml

## Gợi ý test nhanh (Week4)

```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/students
curl "http://127.0.0.1:5000/students?year=2"
```

## Ghi chú

- Dữ liệu đang lưu in-memory, restart server sẽ mất dữ liệu tạo mới.
- Secret/JWT trong ví dụ Week2 phục vụ mục đích học tập, không dùng trực tiếp cho production.