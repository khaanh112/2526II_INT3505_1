# OpenAPI Demo (Library Management)

## File chính
- `openapi.yaml`

## Cài đặt công cụ xem tài liệu
Bạn có thể dùng Swagger UI qua Docker:

```bash
docker run -p 8080:8080 -e SWAGGER_JSON=/foo/openapi.yaml -v ${PWD}:/foo swaggerapi/swagger-ui
```

Hoặc dùng VS Code extension **Swagger Viewer**.

## Endpoint trong demo
- `GET /health`
- `GET /books`
- `GET /books/{bookId}`
- `POST /books`
- `PUT /books/{bookId}`
- `DELETE /books/{bookId}`

## Sinh code (có sẵn)

```bash
npx --yes @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o ../generated/openapi-python-client
```

## Sinh test/contract test (có sẵn)

Chạy server Flask trước ở `http://127.0.0.1:5000`, sau đó:

```bash
npx --yes dredd openapi.yaml http://127.0.0.1:5000
```
