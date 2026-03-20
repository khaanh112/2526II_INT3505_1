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
npx --yes @typespec/compiler compile main.tsp --emit @typespec/openapi3
```

Lệnh trên sẽ tạo file OpenAPI trong thư mục `tsp-output`.

## Endpoint trong demo
- `GET /health`
- `GET /books`, `POST /books`
- `GET /books/{bookId}`, `PUT /books/{bookId}`, `DELETE /books/{bookId}`

## Sinh code/test

TypeSpec sinh OpenAPI trước, sau đó dùng tool OpenAPI:

```bash
npx --yes @openapitools/openapi-generator-cli generate -i tsp-output/@typespec/openapi3/openapi.yaml -g python -o ../generated/typespec-python-client
npx --yes dredd tsp-output/@typespec/openapi3/openapi.yaml http://127.0.0.1:5000
```
