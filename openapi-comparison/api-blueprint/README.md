# API Blueprint Guide

Tài liệu hướng dẫn chuyển đổi từ API Blueprint sang OpenAPI và sinh Code.

## 1. Chuyển đổi sang OpenAPI (Swagger)
Sử dụng công cụ `apib2swagger` để convert:
```bash
npx --yes apib2swagger -i api.apib -o swagger.json
```

## 2. Sinh Server (Flask/Python)
Sau khi có `swagger.json`, dùng lệnh sau để sinh bộ khung Server:
```bash
npx --yes @openapitools/openapi-generator-cli generate -i swagger.json -g python-flask -o ../generated/server-blueprint-flask
```

## 3. Review trực quan
Dùng `aglio` để tạo file HTML đẹp mắt cho API Blueprint:
```bash
npx --yes aglio -i api.apib -o index.html
```
