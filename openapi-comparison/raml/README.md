# RAML Demo (Library Management)

## File chính
- `api.raml`

## Cài đặt công cụ validate

```bash
npm install -g raml-cop
```

## Chạy thử
Validate cú pháp RAML:

```bash
raml-cop api.raml
```

## Render tài liệu (tuỳ chọn)
Bạn có thể dùng API Console hỗ trợ RAML hoặc import file vào Anypoint Platform để xem interactive docs.

## Endpoint đã đồng bộ theo Flask server
- `GET /`
- `GET /health`
- `GET /books`, `POST /books`
- `GET /books/{bookId}`, `PUT /books/{bookId}`, `DELETE /books/{bookId}`
- `GET /members`
- `POST /borrow`
- `POST /return`
- `GET /borrow-records`
