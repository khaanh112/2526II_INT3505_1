# TypeSpec

File: `main.tsp`

Compile ra OpenAPI:

```bash
npx --yes @typespec/compiler compile main.tsp --emit @typespec/openapi3
```

Sau đó dùng tool OpenAPI để sinh code/test:

```bash
npx --yes @openapitools/openapi-generator-cli generate -i tsp-output/@typespec/openapi3/openapi.yaml -g python -o ../generated/typespec-python-client
npx --yes dredd tsp-output/@typespec/openapi3/openapi.yaml http://127.0.0.1:5000
```
