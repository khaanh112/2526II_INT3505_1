# INT3505 - Demo API theo tuần

Repository này chứa các bài thực hành theo từng tuần cho môn INT3505, tập trung vào:
- xây dựng API với Flask,
- tài liệu hoá API bằng OpenAPI/Swagger.

## Cấu trúc thư mục

```text
Week4/
	openapi.yaml
	requirements.txt
	server.py
```

## Yêu cầu môi trường

- Python 3.10+
- pip


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
