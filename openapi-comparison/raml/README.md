# RAML Guide

Tài liệu hướng dẫn chuyển đổi từ RAML sang OpenAPI và sinh Code.

## 1. Chuyển đổi sang OpenAPI (OAS)
Hãy mở Terminal tại thư mục `openapi-comparison/raml`:
```bash
cd openapi-comparison/raml
npx --yes oas-raml-converter --from RAML --to OAS30 api.raml > swagger.json
```
_Lưu ý: Nếu bạn đang ở thư mục gốc, hãy sử dụng đường dẫn đầy đủ thay vì chỉ `api.raml`_

## 2. Sinh Server (Flask/Python)
Dùng OpenAPI Generator để sinh code từ file `swagger.json` vừa tạo:
```bash
npx --yes @openapitools/openapi-generator-cli generate -i swagger.json -g python-flask -o ../generated/server-raml-flask
```

## Lưu ý về RAML
Các công cụ sinh trực tiếp (như `raml-python-cloudant` hay `raml-server-generator`) hiện đã cũ và không còn hỗ trợ tốt RAML 1.0. Quy trình chuyển đổi qua OpenAPI là cách ổn định nhất hiện nay.
