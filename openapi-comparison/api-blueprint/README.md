# API Blueprint

File: `api.apib`

Cài tool:

```bash
npm install -g aglio dredd
```

Xem docs nhanh:

```bash
aglio -i api.apib -s
```

Contract test:

```bash
dredd api.apib http://127.0.0.1:5000
```

Ghi chú: API Blueprint không mạnh về codegen như OpenAPI.
