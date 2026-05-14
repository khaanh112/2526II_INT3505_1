import time
import logging
import random
from flask import Flask, request, jsonify, g
from prometheus_flask_exporter import PrometheusMetrics
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pycircuitbreaker import circuit
from flask_talisman import Talisman

# --- Configuration ---
app = Flask(__name__)

# Security Headers (WAF-like)
# Set force_https=False for local development
Talisman(app, content_security_policy=None, force_https=False) 

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("flask-production-api")

# --- Observability: Metrics ---
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

# --- Rate Limiter Setup ---
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# --- Middleware: Audit Logs ---
@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    if request.path == '/metrics':
        return response
    
    now = time.time()
    duration = round(now - g.start, 4)
    ip = request.remote_addr
    method = request.method
    url = request.url
    status = response.status_code
    
    logger.info(
        f"AUDIT: IP={ip} Method={method} URL={url} "
        f"Status={status} Latency={duration}s"
    )
    return response

# --- Circuit Breaker: Simulated External Service ---
@circuit
def external_service_call():
    if random.random() < 0.3:
        raise Exception("External service failure")
    return {"status": "success", "data": "External Flask Data"}

# --- Endpoints ---

@app.route('/')
def hello():
    return jsonify({"message": "Flask API is healthy", "timestamp": time.time()})

@app.route('/data')
@limiter.limit("5 per minute")
def get_data():
    """
    Returns data with rate limiting (5 requests per minute).
    """
    return jsonify({
        "data": "Sensitive Flask data protected by rate limiting",
        "client": request.remote_addr
    })

@app.route('/external')
def call_external():
    """
    Calls an external service with a circuit breaker.
    """
    try:
        result = external_service_call()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Circuit Breaker Error: {str(e)}")
        return jsonify({"error": "Service temporarily unavailable", "detail": str(e)}), 503

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "ratelimit exceeded", "message": str(e.description)}), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
