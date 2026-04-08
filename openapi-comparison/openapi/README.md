# OpenAPI Guide

Tài liệu hướng dẫn sinh Code từ OpenAPI Specification.

## Sinh Server (Flask/Python)
Lệnh sinh trực tiếp bộ khung Server Flask:
```bash
npx --yes @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-flask -o ../generated/server-openapi-flask
```

## Sinh Client (Python)
Lệnh sinh Client SDK để gọi API:
```bash
npx --yes @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o ../generated/client-openapi-python
```

## Chạy thử (Contract Testing)
Sử dụng Dredd để kiểm tra tính đúng đắn của spec:
```bash
npx --yes dredd openapi.yaml http://127.0.0.1:5000
```
