import copy
import datetime


class StoreError(Exception):
    pass


class OrderNotFound(StoreError):
    pass


class ValidationError(StoreError):
    pass


class InvalidState(StoreError):
    pass


orders_db = [
    {
        "id": 1,
        "customer_name": "Kha Anh",
        "email": "khaanh@example.com",
        "items": [{"name": "Mechanical Keyboard", "price": 89.99, "quantity": 1}],
        "total_amount": 89.99,
        "status": "PENDING",
        "created_at": (datetime.datetime.utcnow() - datetime.timedelta(hours=2)).isoformat() + "Z",
        "updated_at": (datetime.datetime.utcnow() - datetime.timedelta(hours=2)).isoformat() + "Z",
    },
    {
        "id": 2,
        "customer_name": "Minh Tu",
        "email": "minhtu@example.com",
        "items": [
            {"name": "Wireless Mouse", "price": 49.99, "quantity": 1},
            {"name": "Mousepad", "price": 19.99, "quantity": 2},
        ],
        "total_amount": 89.97,
        "status": "PAID",
        "created_at": (datetime.datetime.utcnow() - datetime.timedelta(minutes=45)).isoformat() + "Z",
        "updated_at": (datetime.datetime.utcnow() - datetime.timedelta(minutes=40)).isoformat() + "Z",
    },
]

event_log = []
event_id_counter = 1


def _clone(value):
    return copy.deepcopy(value)


def _now():
    return datetime.datetime.utcnow().isoformat() + "Z"


def _publish_event(event_type, order):
    global event_id_counter

    event = {
        "id": event_id_counter,
        "event_type": event_type,
        "data": _clone(order),
        "timestamp": _now(),
    }
    event_id_counter += 1
    event_log.append(event)
    return event


def list_orders(
    status=None,
    customer=None,
    min_amount=None,
    page=1,
    limit=5,
    sort_by="created_at",
    sort_order="desc",
):
    page = max(int(page or 1), 1)
    limit = max(int(limit or 5), 1)
    filtered = orders_db

    if status:
        filtered = [o for o in filtered if o["status"].upper() == status.upper()]
    if customer:
        filtered = [o for o in filtered if customer.lower() in o["customer_name"].lower()]
    if min_amount not in (None, ""):
        try:
            threshold = float(min_amount)
        except (TypeError, ValueError) as exc:
            raise ValidationError("min_amount must be numeric") from exc
        filtered = [o for o in filtered if o["total_amount"] >= threshold]

    valid_sort_keys = {"id", "customer_name", "total_amount", "created_at", "updated_at"}
    if sort_by not in valid_sort_keys:
        sort_by = "created_at"

    reverse = sort_order.lower() == "desc"
    filtered = sorted(filtered, key=lambda order: order[sort_by], reverse=reverse)

    total_items = len(filtered)
    total_pages = (total_items + limit - 1) // limit if total_items else 1
    page = min(page, total_pages)
    start = (page - 1) * limit
    items = filtered[start : start + limit]

    return {
        "items": _clone(items),
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": total_pages,
    }


def get_order(order_id):
    order = next((o for o in orders_db if o["id"] == int(order_id)), None)
    if order is None:
        raise OrderNotFound(f"Order with ID {order_id} not found")
    return _clone(order)


def create_order(customer_name, email, items):
    if not customer_name or not email or not items:
        raise ValidationError("customer_name, email, and items are required")

    parsed_items = []
    total_amount = 0.0

    for item in items:
        name = item.get("name")
        price = item.get("price")
        quantity = item.get("quantity", 1)

        if not name or price is None:
            raise ValidationError("Each item must have a name and price")

        try:
            price = float(price)
            quantity = int(quantity)
        except (TypeError, ValueError) as exc:
            raise ValidationError("price must be numeric, quantity must be integer") from exc

        parsed_items.append({"name": name, "price": price, "quantity": quantity})
        total_amount += price * quantity

    order_id = max([order["id"] for order in orders_db], default=0) + 1
    timestamp = _now()
    order = {
        "id": order_id,
        "customer_name": customer_name,
        "email": email,
        "items": parsed_items,
        "total_amount": round(total_amount, 2),
        "status": "PENDING",
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    orders_db.append(order)
    _publish_event("order.created", order)
    return _clone(order)


def transition_order(order_id, action):
    order = next((o for o in orders_db if o["id"] == int(order_id)), None)
    if order is None:
        raise OrderNotFound(f"Order with ID {order_id} not found")

    transitions = {
        "pay": ("PENDING", "PAID", "order.paid"),
        "cancel": ("PENDING", "CANCELLED", "order.cancelled"),
        "ship": ("PAID", "SHIPPED", "order.shipped"),
    }
    if action not in transitions:
        raise ValidationError(f"Unsupported transition: {action}")

    expected, next_status, event_type = transitions[action]
    if order["status"] != expected:
        raise InvalidState(f"Order cannot {action} from status {order['status']}")

    order["status"] = next_status
    order["updated_at"] = _now()
    _publish_event(event_type, order)
    return _clone(order)


def list_events():
    return _clone(event_log)
