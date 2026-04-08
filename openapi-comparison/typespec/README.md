# TypeSpec Guide

Tài liệu hướng dẫn biên dịch TypeSpec sang OpenAPI và sinh Code.

## 1. Biên dịch sang OpenAPI
Dùng trình biên dịch của TypeSpec (yêu cầu file `tspconfig.yaml` phải cấu hình emitter `openapi3`):
```bash
npx --yes @typespec/compiler compile .
```
Lệnh này mặc định sẽ tạo file tại thư mục `tsp-output/@typespec/openapi3/openapi.yaml`.

## 2. Sinh Server (Flask/Python)
Sinh code từ file kết quả của TypeSpec:
```bash
npx --yes @openapitools/openapi-generator-cli generate -i tsp-output/@typespec/openapi3/openapi.yaml -g python-flask -o ../generated/server-typespec-flask
```

## Setup nhanh
Nếu bạn chưa cài đặt môi trường TypeSpec:
```bash
npm install -g @typespec/compiler @typespec/openapi3
```
