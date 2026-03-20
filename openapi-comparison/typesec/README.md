# TypeSpec Demo (Library Management)

## File chính
- `main.tsp`

> Ghi chú: trong hệ sinh thái hiện tại, format tương ứng phổ biến là **TypeSpec**.

## Cài đặt

```bash
npm install -g @typespec/compiler @typespec/http @typespec/openapi3
```

## Compile sang OpenAPI

```bash
tsp compile .
```

Lệnh trên sẽ tạo file OpenAPI trong thư mục `tsp-output`.

## Xem bằng Swagger UI
Sau khi compile, mở file OpenAPI sinh ra bằng Swagger UI hoặc Swagger Viewer extension trong VS Code.

## Endpoint đã đồng bộ theo Flask server
- `GET /`
- `GET /health`
- `GET /books`, `POST /books`
- `GET /books/{bookId}`, `PUT /books/{bookId}`, `DELETE /books/{bookId}`
- `GET /members`
- `POST /borrow`
- `POST /return`
- `GET /borrow-records`
