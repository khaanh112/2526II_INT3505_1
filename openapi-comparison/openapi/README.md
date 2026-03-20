# OpenAPI

File: `openapi.yaml`

Endpoints trong demo:
- `GET /health`
- `GET /books`
- `GET /books/{bookId}`
- `POST /books`
- `PUT /books/{bookId}`
- `DELETE /books/{bookId}`

Sinh Python client:

```bash
npx --yes @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o ../generated/openapi-python-client
```

Contract test:

```bash
npx --yes dredd openapi.yaml http://127.0.0.1:5000
```
