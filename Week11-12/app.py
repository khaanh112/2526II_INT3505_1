import datetime
import logging
import threading
import requests
from flask import Flask, request, jsonify

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("week1112-api")

app = Flask(__name__)

# In-memory database
orders_db = [
    {
        "id": 1,
        "customer_name": "Kha Anh",
        "email": "khaanh@example.com",
        "items": [{"name": "Mechanical Keyboard", "price": 89.99, "quantity": 1}],
        "total_amount": 89.99,
        "status": "PENDING",
        "created_at": (datetime.datetime.utcnow() - datetime.timedelta(hours=2)).isoformat() + "Z",
        "updated_at": (datetime.datetime.utcnow() - datetime.timedelta(hours=2)).isoformat() + "Z"
    },
    {
        "id": 2,
        "customer_name": "Minh Tu",
        "email": "minhtu@example.com",
        "items": [
            {"name": "Wireless Mouse", "price": 49.99, "quantity": 1},
            {"name": "Mousepad", "price": 19.99, "quantity": 2}
        ],
        "total_amount": 89.97,
        "status": "PAID",
        "created_at": (datetime.datetime.utcnow() - datetime.timedelta(minutes=45)).isoformat() + "Z",
        "updated_at": (datetime.datetime.utcnow() - datetime.timedelta(minutes=40)).isoformat() + "Z"
    }
]

# Webhook databases & dispatcher
webhook_subscriptions = []
event_log = []
subscription_id_counter = 1
event_id_counter = 1

def dispatch_webhook(event_type, event_data):
    global event_id_counter
    event_id = event_id_counter
    event_id_counter += 1
    
    event_entry = {
        "id": event_id,
        "event_type": event_type,
        "data": event_data,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    event_log.append(event_entry)
    logger.info(f"Event published: {event_type} (Event ID: {event_id})")
    
    def send_to_subscribers():
        for sub in webhook_subscriptions:
            if event_type in sub["events"] or "*" in sub["events"]:
                target_url = sub["target_url"]
                logger.info(f"Dispatching event {event_type} to subscriber {target_url}")
                try:
                    response = requests.post(target_url, json=event_entry, timeout=5)
                    logger.info(f"Webhook response from {target_url}: Status {response.status_code}")
                except Exception as e:
                    logger.error(f"Failed to deliver webhook to {target_url}: {e}")
                    
    threading.Thread(target=send_to_subscribers, daemon=True).start()

def add_hateoas_links(order):
    order_id = order["id"]
    status = order["status"]
    
    links = {
        "self": {
            "href": f"/api/orders/{order_id}",
            "method": "GET",
            "rel": "self"
        },
        "update": {
            "href": f"/api/orders/{order_id}",
            "method": "PUT",
            "rel": "update"
        },
        "delete": {
            "href": f"/api/orders/{order_id}",
            "method": "DELETE",
            "rel": "delete"
        }
    }
    
    if status == "PENDING":
        links["pay"] = {
            "href": f"/api/orders/{order_id}/pay",
            "method": "POST",
            "rel": "payment"
        }
        links["cancel"] = {
            "href": f"/api/orders/{order_id}/cancel",
            "method": "POST",
            "rel": "cancel"
        }
    elif status == "PAID":
        links["ship"] = {
            "href": f"/api/orders/{order_id}/ship",
            "method": "POST",
            "rel": "shipment"
        }
    
    order_copy = dict(order)
    order_copy["_links"] = links
    return order_copy

# Root entry point
@app.route("/")
def index():
    return jsonify({
        "message": "Welcome to the Order Management System (OMS) API",
        "version": "1.0.0",
        "description": "Pure backend REST API showcasing CRUD, Query, HATEOAS, EDA, and Webhook patterns."
    })

# 1. READ ALL with Query Pattern (filtering, sorting, pagination)
@app.route("/api/orders", methods=["GET"])
def get_orders():
    # Filtering query parameters
    status = request.args.get("status")
    customer = request.args.get("customer")
    min_amount_raw = request.args.get("min_amount")
    
    # Sorting query parameters
    sort_by = request.args.get("sort_by", default="created_at")
    sort_order = request.args.get("order", default="desc").lower()
    
    # Pagination query parameters
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=5, type=int)
    
    if page < 1: page = 1
    if limit < 1: limit = 5
    
    filtered_orders = orders_db
    
    # Apply filters
    if status:
        filtered_orders = [o for o in filtered_orders if o["status"].upper() == status.upper()]
    if customer:
        filtered_orders = [o for o in filtered_orders if customer.lower() in o["customer_name"].lower()]
    if min_amount_raw:
        try:
            min_amount = float(min_amount_raw)
            filtered_orders = [o for o in filtered_orders if o["total_amount"] >= min_amount]
        except ValueError:
            pass

    # Sort operation
    valid_sort_keys = ["id", "customer_name", "total_amount", "created_at", "updated_at"]
    if sort_by not in valid_sort_keys:
        sort_by = "created_at"
        
    reverse = (sort_order == "desc")
    filtered_orders = sorted(filtered_orders, key=lambda x: x[sort_by], reverse=reverse)

    # Paginate operation
    total_items = len(filtered_orders)
    total_pages = (total_items + limit - 1) // limit if total_items > 0 else 1
    
    if page > total_pages:
        page = total_pages
        
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_orders = filtered_orders[start_idx:end_idx]

    # Map HATEOAS links to each item
    hateoas_orders = [add_hateoas_links(o) for o in paginated_orders]
    
    # Collection links
    links = {
        "self": {"href": f"/api/orders?page={page}&limit={limit}", "method": "GET"},
        "create": {"href": "/api/orders", "method": "POST"}
    }
    if page > 1:
        links["prev"] = {"href": f"/api/orders?page={page-1}&limit={limit}", "method": "GET"}
    if page < total_pages:
        links["next"] = {"href": f"/api/orders?page={page+1}&limit={limit}", "method": "GET"}
        
    return jsonify({
        "items": hateoas_orders,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "_links": links
    })

# 2. READ ONE
@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "NOT_FOUND", "message": f"Order with ID {order_id} not found"}), 404
    return jsonify(add_hateoas_links(order))

# 3. CREATE
@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "INVALID_BODY", "message": "JSON request body is required"}), 400
        
    customer_name = data.get("customer_name")
    email = data.get("email")
    items = data.get("items", [])
    
    if not customer_name or not email or not items:
        return jsonify({"error": "VALIDATION_FAILED", "message": "customer_name, email, and items are required"}), 400
        
    total_amount = 0.0
    parsed_items = []
    for it in items:
        name = it.get("name")
        price = it.get("price")
        qty = it.get("quantity", 1)
        if not name or price is None:
            return jsonify({"error": "VALIDATION_FAILED", "message": "Each item must have a name and price"}), 400
        try:
            price = float(price)
            qty = int(qty)
        except ValueError:
            return jsonify({"error": "VALIDATION_FAILED", "message": "price must be numeric, quantity must be integer"}), 400
            
        total_amount += price * qty
        parsed_items.append({"name": name, "price": price, "quantity": qty})

    order_id = max([o["id"] for o in orders_db]) + 1 if orders_db else 1
    now = datetime.datetime.utcnow().isoformat() + "Z"
    
    new_order = {
        "id": order_id,
        "customer_name": customer_name,
        "email": email,
        "items": parsed_items,
        "total_amount": round(total_amount, 2),
        "status": "PENDING",
        "created_at": now,
        "updated_at": now
    }
    
    orders_db.append(new_order)
    dispatch_webhook("order.created", new_order)
    return jsonify(add_hateoas_links(new_order)), 201

# 4. UPDATE
@app.route("/api/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "NOT_FOUND", "message": f"Order with ID {order_id} not found"}), 404
        
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "INVALID_BODY", "message": "JSON body is required"}), 400
        
    customer_name = data.get("customer_name")
    email = data.get("email")
    items = data.get("items")
    
    if customer_name:
        order["customer_name"] = customer_name
    if email:
        order["email"] = email
        
    if items is not None:
        total_amount = 0.0
        parsed_items = []
        for it in items:
            name = it.get("name")
            price = it.get("price")
            qty = it.get("quantity", 1)
            if not name or price is None:
                return jsonify({"error": "VALIDATION_FAILED", "message": "Each item must have a name and price"}), 400
            try:
                price = float(price)
                qty = int(qty)
            except ValueError:
                return jsonify({"error": "VALIDATION_FAILED", "message": "price must be numeric, quantity must be integer"}), 400
            total_amount += price * qty
            parsed_items.append({"name": name, "price": price, "quantity": qty})
        order["items"] = parsed_items
        order["total_amount"] = round(total_amount, 2)
        
    order["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    return jsonify(add_hateoas_links(order))

# 5. DELETE
@app.route("/api/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    global orders_db
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "NOT_FOUND", "message": f"Order with ID {order_id} not found"}), 404
        
    orders_db = [o for o in orders_db if o["id"] != order_id]
    return jsonify({"success": True, "message": f"Order {order_id} has been successfully deleted"})

# 6. STATE TRANSITIONS (HATEOAS Actions)
@app.route("/api/orders/<int:order_id>/pay", methods=["POST"])
def pay_order(order_id):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "NOT_FOUND", "message": f"Order with ID {order_id} not found"}), 404
        
    if order["status"] != "PENDING":
        return jsonify({"error": "INVALID_STATE", "message": f"Order cannot be paid from status {order['status']}"}), 400
        
    order["status"] = "PAID"
    order["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    dispatch_webhook("order.paid", order)
    return jsonify(add_hateoas_links(order))

@app.route("/api/orders/<int:order_id>/cancel", methods=["POST"])
def cancel_order(order_id):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "NOT_FOUND", "message": f"Order with ID {order_id} not found"}), 404
        
    if order["status"] != "PENDING":
        return jsonify({"error": "INVALID_STATE", "message": f"Order cannot be cancelled from status {order['status']}"}), 400
        
    order["status"] = "CANCELLED"
    order["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    dispatch_webhook("order.cancelled", order)
    return jsonify(add_hateoas_links(order))

@app.route("/api/orders/<int:order_id>/ship", methods=["POST"])
def ship_order(order_id):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "NOT_FOUND", "message": f"Order with ID {order_id} not found"}), 404
        
    if order["status"] != "PAID":
        return jsonify({"error": "INVALID_STATE", "message": f"Order cannot be shipped from status {order['status']}"}), 400
        
    order["status"] = "SHIPPED"
    order["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    dispatch_webhook("order.shipped", order)
    return jsonify(add_hateoas_links(order))

# 7. WEBHOOK SUBSCRIPTIONS AND EVENTS
@app.route("/api/webhooks/subscriptions", methods=["POST"])
def create_webhook_subscription():
    global subscription_id_counter
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "INVALID_BODY", "message": "JSON body is required"}), 400
        
    target_url = data.get("target_url")
    events = data.get("events", [])
    
    if not target_url or not events:
        return jsonify({"error": "VALIDATION_FAILED", "message": "target_url and events list are required"}), 400
        
    if not isinstance(events, list):
        return jsonify({"error": "VALIDATION_FAILED", "message": "events must be a list of strings"}), 400
        
    sub_id = subscription_id_counter
    subscription_id_counter += 1
    
    new_sub = {
        "id": sub_id,
        "target_url": target_url,
        "events": [e.lower() for e in events],
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    webhook_subscriptions.append(new_sub)
    return jsonify(new_sub), 201

@app.route("/api/webhooks/subscriptions", methods=["GET"])
def get_webhook_subscriptions():
    return jsonify(webhook_subscriptions)

@app.route("/api/webhooks/subscriptions/<int:sub_id>", methods=["DELETE"])
def delete_webhook_subscription(sub_id):
    global webhook_subscriptions
    sub = next((s for s in webhook_subscriptions if s["id"] == sub_id), None)
    if not sub:
        return jsonify({"error": "NOT_FOUND", "message": f"Subscription with ID {sub_id} not found"}), 404
        
    webhook_subscriptions = [s for s in webhook_subscriptions if s["id"] != sub_id]
    return jsonify({"success": True, "message": f"Webhook subscription {sub_id} has been deleted"})

@app.route("/api/webhooks/events", methods=["GET"])
def get_webhook_events():
    return jsonify(event_log)

if __name__ == "__main__":
    logger.info("Starting Week 11-12 API on port 8000...")
    app.run(host="0.0.0.0", port=8000, debug=True)
