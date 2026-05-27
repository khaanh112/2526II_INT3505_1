from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def developer_portal():
    return jsonify({
        "name": "Week 13 API Product Demo",
        "tagline": "Treat an API as a product for developers.",
        "version": "1.0.0",
        "links": {
            "health": "/health",
            "docs": "/api/docs",
            "plans": "/api/plans",
            "register": "/api/developers/register",
            "sandbox": "/api/sandbox/weather?city=Hanoi",
            "analytics": "/api/analytics/kpis"
        }
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/docs")
def api_docs():
    return jsonify({
        "title": "Weather Insights API",
        "audience": "Developers building dashboards, travel apps, and logistics tools.",
        "quickstart": [
            "Register a developer account to receive an API key.",
            "Call sandbox endpoints with the X-API-Key header.",
            "Track usage and errors from the analytics endpoint."
        ]
    })


@app.route("/api/plans")
def pricing_plans():
    return jsonify({
        "plans": [
            {
                "id": "free",
                "name": "Free",
                "monthly_fee_usd": 0,
                "included_calls": 1000,
                "overage_usd_per_call": 0.002
            }
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8013, debug=True)
