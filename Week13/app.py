import datetime
import time
import uuid

from flask import Flask, g, jsonify, request

app = Flask(__name__)

developers = {}
api_keys = {}
usage_events = []

PRICING_PLANS = {
    "free": {
        "id": "free",
        "name": "Free",
        "monthly_fee_usd": 0,
        "included_calls": 1000,
        "overage_usd_per_call": 0.002,
        "best_for": "Students, prototypes, and sandbox evaluation"
    },
    "growth": {
        "id": "growth",
        "name": "Growth",
        "monthly_fee_usd": 49,
        "included_calls": 50000,
        "overage_usd_per_call": 0.001,
        "best_for": "Small products with predictable traffic"
    },
    "enterprise": {
        "id": "enterprise",
        "name": "Enterprise",
        "monthly_fee_usd": None,
        "included_calls": "custom",
        "overage_usd_per_call": "contract",
        "best_for": "High-volume teams needing SLA, support, and invoices"
    }
}

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


@app.before_request
def start_request_timer():
    g.started_at = time.perf_counter()


@app.after_request
def collect_usage_event(response):
    if not request.path.startswith("/api/") or request.path == "/api/analytics/kpis":
        return response

    raw_key = request.headers.get("X-API-Key")
    developer_id = api_keys.get(raw_key)
    usage_events.append({
        "timestamp": utc_now(),
        "method": request.method,
        "path": request.path,
        "status_code": response.status_code,
        "developer_id": developer_id,
        "latency_ms": round((time.perf_counter() - g.started_at) * 1000, 2)
    })
    return response


def plan_mix():
    counts = {}
    for developer in developers.values():
        plan = developer["plan"]
        counts[plan] = counts.get(plan, 0) + 1
    return counts


def calls_by_endpoint():
    counts = {}
    for event in usage_events:
        key = f"{event['method']} {event['path']}"
        counts[key] = counts.get(key, 0) + 1
    return counts


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
        "positioning": "Freemium for adoption, pay-per-call for scalable revenue.",
        "plans": list(PRICING_PLANS.values())
    })


@app.route("/api/monetization")
def monetization_model():
    return jsonify({
        "model": "freemium + pay-per-call",
        "why_it_fits": [
            "Free sandbox removes friction for new developers.",
            "Usage-based overage aligns revenue with delivered API value.",
            "Enterprise tier supports SLA, priority support, and custom volume."
        ],
        "billing_metrics": [
            "successful_api_calls",
            "premium_endpoint_calls",
            "support_sla"
        ],
        "guardrails": [
            "Publish quota and overage price clearly in the portal.",
            "Send usage alerts before developers exceed included calls.",
            "Keep sandbox free but rate-limited."
        ]
    })


@app.route("/api/launch-strategy")
def launch_strategy():
    return jsonify({
        "goal": "Make the first successful API call happen in under 5 minutes.",
        "phases": [
            {
                "name": "Private beta",
                "actions": [
                    "Invite 10-20 developers from target use cases.",
                    "Collect feedback on docs, sample code, and error messages.",
                    "Track activation: registered developers who make one sandbox call."
                ]
            },
            {
                "name": "Public launch",
                "actions": [
                    "Publish developer portal, OpenAPI file, quickstart, and changelog.",
                    "Offer free tier and visible upgrade path.",
                    "Add support channel and status page link."
                ]
            },
            {
                "name": "Growth",
                "actions": [
                    "Add SDKs for the most active languages.",
                    "Review analytics weekly: call volume, error rate, and retention.",
                    "Use case studies to convert free developers to paid plans."
                ]
            }
        ],
        "developer_experience_assets": [
            "developer portal",
            "interactive docs",
            "sandbox API key",
            "OpenAPI contract",
            "sample curl requests"
        ]
    })


@app.route("/api/analytics/kpis")
def analytics_kpis():
    call_volume = len(usage_events)
    error_count = len([event for event in usage_events if event["status_code"] >= 400])
    error_rate = round(error_count / call_volume, 4) if call_volume else 0

    return jsonify({
        "developer_registrations": len(developers),
        "active_api_keys": len(api_keys),
        "call_volume": call_volume,
        "error_count": error_count,
        "error_rate": error_rate,
        "plan_mix": plan_mix(),
        "calls_by_endpoint": calls_by_endpoint(),
        "recent_events": usage_events[-10:]
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
    if plan not in PRICING_PLANS:
        return jsonify({
            "error": "UNKNOWN_PLAN",
            "message": f"plan must be one of: {', '.join(PRICING_PLANS.keys())}"
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
