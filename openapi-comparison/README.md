# OpenAPI Comparison (Library Demo)

Demo nhỏ để so sánh 4 format tài liệu API: **OpenAPI, API Blueprint, RAML, TypeSpec**.

## Cấu trúc

- `openapi/openapi.yaml`
- `api-blueprint/api.apib`
- `raml/api.raml`
- `typesec/main.tsp`

Mỗi thư mục con có `README.md` riêng với lệnh cài đặt/chạy.

## API demo (đơn giản)

- `GET /health`
- `GET /books`
- `GET /books/<book_id>`
- `POST /books`
- `PUT /books/<book_id>`
- `DELETE /books/<book_id>`

## Chạy server Flask

```bash
pip install flask
python server.py
```

Server chạy ở `http://127.0.0.1:5000`.

## So sánh nhanh

| Format | Mục tiêu chính | Sinh code có sẵn | Sinh test có sẵn |
|---|---|---|---|
| OpenAPI | Chuẩn phổ biến nhất, hệ sinh thái mạnh | Có (`openapi-generator`) | Có công cụ phổ biến từ spec (`dredd`, `schemathesis`) |
| API Blueprint | Viết docs dễ đọc, thiên về mô tả | Không có chuẩn codegen phổ biến như OpenAPI | Có `dredd` chạy API contract test từ `.apib` |
| RAML | Mạnh trong hệ sinh thái Mule/Anypoint | Có trong hệ sinh thái Mule (APIkit), ngoài hệ này không phổ biến | Không có 1 chuẩn test tool phổ biến độc lập như OpenAPI |
| TypeSpec | Ngôn ngữ mô hình API, sinh spec | Sinh OpenAPI qua `tsp compile`, sau đó codegen bằng tool OpenAPI | Sinh OpenAPI trước, sau đó test bằng tool OpenAPI |

## Demo sinh code/test bằng công cụ có sẵn

### 1) OpenAPI

Sinh Python client:

```bash
npx --yes @openapitools/openapi-generator-cli generate -i openapi/openapi.yaml -g python -o generated/openapi-python-client
```

Contract test với Dredd:

```bash
npx --yes dredd openapi/openapi.yaml http://127.0.0.1:5000
```

### 2) API Blueprint

Contract test trực tiếp từ `.apib` bằng Dredd:

```bash
npx --yes dredd api-blueprint/api.apib http://127.0.0.1:5000
```

### 3) RAML

RAML không có workflow codegen/test CLI độc lập phổ biến như OpenAPI trong repo demo này.
Thực tế thường dùng trong hệ sinh thái Mule/Anypoint (APIkit).

### 4) TypeSpec

Compile TypeSpec thành OpenAPI:

```bash
npx --yes @typespec/compiler compile typesec/main.tsp --emit @typespec/openapi3
```

Sau đó dùng OpenAPI tool để sinh code/test (giống phần OpenAPI).
