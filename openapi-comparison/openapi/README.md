# OpenAPI Demo (Library Management)

## File chính
- `openapi.yaml`

## Cài đặt công cụ xem tài liệu
Bạn có thể dùng Swagger UI qua Docker:

```bash
docker run -p 8080:8080 -e SWAGGER_JSON=/foo/openapi.yaml -v ${PWD}:/foo swaggerapi/swagger-ui
```

Hoặc dùng VS Code extension **Swagger Viewer**.

## Chạy thử
1. Di chuyển vào thư mục này.
2. Mở `http://localhost:8080` nếu chạy bằng Docker.
3. Thử các endpoint: `/`, `/health`, `/books`, `/members`, `/borrow`, `/return`, `/borrow-records`.

## Lưu ý đồng bộ với Flask server
- Server chạy mặc định ở `http://localhost:5000`.
- Cấu trúc response chuẩn:
	- Thành công: `{ "success": true, "message": "...", "data": ... }`
	- Lỗi: `{ "success": false, "error": "..." }`

## Generate client/server code (tuỳ chọn)

```bash
npx --yes @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o generated/python-client
```
