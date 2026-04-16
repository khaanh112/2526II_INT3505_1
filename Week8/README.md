# Week 8: Simple Flask API with Automation & Performance Testing

Dự án này là phiên bản rút gọn của User API, được viết thủ công bằng Flask để phục vụ việc học tập về Test tự động và Load testing.

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
Nếu bạn chưa cài đặt Newman toàn cục, bạn có thể sử dụng `npx`:
```bash
npx newman run postman/collection.json
```
Hoặc cài đặt toàn cục bằng npm: `npm install -g newman`.

### Kiểm thử hiệu năng (Locust)
```bash
locust -f performance/locustfile.py --host http://localhost:8080
```
- Truy cập `http://localhost:8089` để xem biểu đồ response time và error rate.

## 4. Các yêu cầu đạt được
- **Unit/Integration Test:** Đã triển khai trong `tests/`.
- **Postman/Newman:** Bộ test endpoint hoàn chỉnh.
- **Load Testing:** Đo hiệu năng thực tế của Flask.
