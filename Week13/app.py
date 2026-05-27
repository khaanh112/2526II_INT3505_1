import datetime
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)

developers = {}
api_keys = {}

SAMPLE_WEATHER = {
    "hanoi": {"city": "Hanoi", "temperature_c": 31, "condition": "Cloudy", "humidity": 72},
    "danang": {"city": "Da Nang", "temperature_c": 29, "condition": "Sunny", "humidity": 65},
    "hochiminh": {"city": "Ho Chi Minh City", "temperature_c": 33, "condition": "Partly cloudy", "humidity": 70}
}


def utc_now():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def find_developer_by_key():
    raw_key = request.headers.get("X-API-Key")
    developer_id = api_keys.get(raw_key)
    if not developer_id:
        return None
    return developers.get(developer_id)


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


@app.route("/api/developers/register", methods=["POST"])
def register_developer():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    company = data.get("company", "Independent")
    plan = data.get("plan", "free")

    if not name or not email:
        return jsonify({
            "error": "VALIDATION_FAILED",
            "message": "name and email are required"
        }), 400

    developer_id = str(len(developers) + 1)
    api_key = f"wk13_{uuid.uuid4().hex[:24]}"
    developer = {
        "id": developer_id,
        "name": name,
        "email": email,
        "company": company,
        "plan": plan,
        "created_at": utc_now()
    }

    developers[developer_id] = developer
    api_keys[api_key] = developer_id

    return jsonify({
        "developer": developer,
        "api_key": api_key,
        "next_steps": [
            "Read /api/docs",
            "Call /api/sandbox/weather?city=Hanoi with X-API-Key",
            "Review /api/analytics/kpis"
        ]
    }), 201


@app.route("/api/developers")
def list_developers():
    return jsonify({"items": list(developers.values()), "total": len(developers)})


@app.route("/api/sandbox/weather")
def sandbox_weather():
    developer = find_developer_by_key()
    if not developer:
        return jsonify({
            "error": "UNAUTHORIZED",
            "message": "Provide a valid X-API-Key header from /api/developers/register"
        }), 401

    city = request.args.get("city", "Hanoi").lower().replace(" ", "")
    weather = SAMPLE_WEATHER.get(city)
    if not weather:
        return jsonify({
            "error": "CITY_NOT_FOUND",
            "message": "Sandbox supports Hanoi, Da Nang, and Ho Chi Minh City"
        }), 404

    return jsonify({
        "data": weather,
        "sandbox": True,
        "served_for": {
            "developer_id": developer["id"],
            "plan": developer["plan"]
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8013, debug=True)
