# API Blueprint Demo (Library Management)

## File chính
- `api.apib`

## Cài đặt công cụ render tài liệu

```bash
npm install -g aglio
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

## Endpoint đã đồng bộ theo Flask server
- `GET /`
- `GET /health`
- `GET /books`, `POST /books`
- `GET /books/{bookId}`, `PUT /books/{bookId}`, `DELETE /books/{bookId}`
- `GET /members`
- `POST /borrow`
- `POST /return`
- `GET /borrow-records`
