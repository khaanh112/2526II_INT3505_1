# Flask Library Demo

Demo nhỏ quản lý thư viện bằng Flask (in-memory data).

## Chạy nhanh

```bash
pip install flask
python server.py
```

Chạy tại: `http://127.0.0.1:5000`

## API chính

- `GET /docs` - danh sách endpoint tài liệu API
- `GET /docs/swagger` - mở Swagger UI (đọc từ OpenAPI hiện tại)
- `GET /docs/openapi.yaml` - file OpenAPI
- `GET /docs/api.apib` - file API Blueprint
- `GET /docs/api.raml` - file RAML
- `GET /docs/main.tsp` - file TypeSpec
- `GET /books` - danh sách sách (hỗ trợ `?q=keyword&available=true|false`)
- `GET /books/<book_id>` - chi tiết sách
- `POST /books` - thêm sách
- `PUT /books/<book_id>` - cập nhật sách
- `DELETE /books/<book_id>` - xoá sách (chỉ khi chưa được mượn)
- `GET /members` - danh sách thành viên
- `POST /borrow` - mượn sách
- `POST /return` - trả sách
- `GET /borrow-records` - lịch sử mượn/trả

## Ví dụ body

### POST /books

```json
{
  "title": "Domain-Driven Design",
  "author": "Eric Evans",
  "year": 2003
}
```

### POST /borrow

```json
{
  "book_id": 1,
  "member_id": 2
}
```

### POST /return

```json
{
  "book_id": 1
}
```
