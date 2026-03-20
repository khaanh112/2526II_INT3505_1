# API Blueprint Demo (Library Management)

## File chính
- `api.apib`

## Cài đặt công cụ docs/test

```bash
npm install -g aglio
npm install -g dredd
```

## Chạy thử
Render thành HTML:

```bash
aglio -i api.apib -o docs.html
```

Preview trực tiếp:

```bash
aglio -i api.apib -s
```

Sau đó mở địa chỉ hiển thị trong terminal (thường là `http://127.0.0.1:3000`).

## Endpoint trong demo
- `GET /health`
- `GET /books`, `POST /books`
- `GET /books/{bookId}`, `PUT /books/{bookId}`, `DELETE /books/{bookId}`

## Sinh test/contract test (có sẵn)

Chạy server Flask trước ở `http://127.0.0.1:5000`, sau đó:

```bash
dredd api.apib http://127.0.0.1:5000
```

## Sinh code

API Blueprint không có chuẩn code generator phổ biến và ổn định như OpenAPI.
