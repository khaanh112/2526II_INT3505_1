# Week 8: Simple Flask API with Automation & Performance Testing

## 1. Cấu trúc dự án
- `app.py`: Mã nguồn chính của API.
- `tests/`: Chứa các bộ test tự động (Unit & Integration).
- `postman/`: Collection để test bằng Postman/Newman.
- `performance/`: Script đo hiệu năng bằng Locust.

## 2. Cách chạy ứng dụng
1. Cài đặt thư viện:
   ```bash
   pip install -r requirements.txt
   ```
2. Chạy API:
   ```bash
   python app.py
   ```

## 3. Chạy các bộ Test

### Kiểm thử tự động (Pytest/Unittest)
```bash
python tests/test_automated.py
```

### Kiểm thử bằng Newman (Postman CLI)
```bash
npx newman run postman/collection.json
```

### Kiểm thử hiệu năng (Locust)
```bash
locust -f performance/locustfile.py --host http://localhost:8080
```

