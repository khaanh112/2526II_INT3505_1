# Week 13: API as a Product

Demo nay minh hoa cach bien API thanh mot san pham cho developer:

- developer experience: portal, docs, sandbox, API key
- monetization: freemium, pay-per-call, enterprise SLA
- analytics: developer registrations, call volume, error rate, plan mix
- launch strategy: private beta, public launch, growth

## Files

- `app.py`: Flask API demo.
- `openapi.yaml`: OpenAPI 3.0 contract cho cac endpoint chinh.
- `tests/test_app.py`: pytest cho onboarding, sandbox va KPI analytics.
- `requirements.txt`: Flask va pytest.

## Run local

```bash
cd Week13
pip install -r requirements.txt
python app.py
```

Server chay tai `http://localhost:8013`.

## Quick test with curl

Register developer:

```bash
curl -X POST http://localhost:8013/api/developers/register \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Minh\",\"email\":\"minh@example.com\",\"plan\":\"free\"}"
```

Call sandbox with the returned API key:

```bash
curl "http://localhost:8013/api/sandbox/weather?city=Hanoi" \
  -H "X-API-Key: wk13_REPLACE_ME"
```

View product KPIs:

```bash
curl http://localhost:8013/api/analytics/kpis
```

## Useful endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Developer portal entry point |
| `GET /api/docs` | Quickstart docs metadata |
| `GET /api/plans` | Pricing tiers |
| `GET /api/monetization` | Monetization model |
| `GET /api/launch-strategy` | API launch plan |
| `POST /api/developers/register` | Developer signup and API key generation |
| `GET /api/sandbox/weather` | Sandbox product API |
| `GET /api/analytics/kpis` | API product KPIs |

## Run tests

```bash
cd Week13
pytest
```
