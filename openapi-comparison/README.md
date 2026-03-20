# So sánh tài liệu API (demo nhỏ)

Repo này có 4 format:
- `openapi/openapi.yaml`
- `api-blueprint/api.apib`
- `raml/api.raml`
- `typesec/main.tsp`

API demo (Flask, in-memory):
- `GET /health`
- `GET /books`
- `GET /books/<book_id>`
- `POST /books`
- `PUT /books/<book_id>`
- `DELETE /books/<book_id>`

Chạy server:

```bash
pip install flask
python server.py
```

Base URL: `http://127.0.0.1:5000`

## So sánh nhanh

- **OpenAPI**: mạnh nhất về codegen/test (`openapi-generator`, `dredd`, `schemathesis`).
- **API Blueprint**: viết docs dễ đọc; test được bằng `dredd`; codegen không mạnh như OpenAPI.
- **RAML**: hợp hệ Mule/Anypoint (APIkit); ngoài hệ đó thì tool codegen/test ít phổ biến.
- **TypeSpec**: viết spec bằng ngôn ngữ riêng, compile ra OpenAPI rồi dùng tool OpenAPI để codegen/test.

## Demo sinh code/test bằng tool có sẵn

OpenAPI codegen:

```bash
npx --yes @openapitools/openapi-generator-cli generate -i openapi/openapi.yaml -g python -o generated/openapi-python-client
```

OpenAPI contract test:

```bash
npx --yes dredd openapi/openapi.yaml http://127.0.0.1:5000
```

API Blueprint contract test:

```bash
npx --yes dredd api-blueprint/api.apib http://127.0.0.1:5000
```

TypeSpec -> OpenAPI:

```bash
npx --yes @typespec/compiler compile typesec/main.tsp --emit @typespec/openapi3
```
