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

## Endpoint trong demo
- `GET /health`
- `GET /books`, `POST /books`
- `GET /books/{bookId}`, `PUT /books/{bookId}`, `DELETE /books/{bookId}`

## Sinh code/test

- Sinh code: trong thực tế chủ yếu dùng MuleSoft APIkit (hệ sinh thái Anypoint).
- Sinh test: không có một CLI phổ biến độc lập như OpenAPI/Dredd trong demo này.
