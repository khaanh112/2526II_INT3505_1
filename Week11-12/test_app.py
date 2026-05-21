import unittest
import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from app import app, webhook_subscriptions, event_log, orders_db

# Simple mock server to receive webhooks
received_webhooks = []

class WebhookReceiverHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_webhooks.append(json.loads(post_data.decode('utf-8')))
        self.send_response(200)
        self.end_headers()
        
    def log_message(self, format, *args):
        # Suppress logging of mock server to keep test output clean
        return

def run_mock_server(server):
    server.serve_forever()

class TestWeek1112API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start a local webhook receiver server
        cls.mock_server = HTTPServer(('127.0.0.1', 8081), WebhookReceiverHandler)
        cls.server_thread = threading.Thread(target=run_mock_server, args=(cls.mock_server,), daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_server.shutdown()
        cls.mock_server.server_close()

    def setUp(self):
        self.client = app.test_client()
        # Reset in-memory databases before each test
        orders_db.clear()
        orders_db.extend([
            {
                "id": 1,
                "customer_name": "Kha Anh",
                "email": "khaanh@example.com",
                "items": [{"name": "Mechanical Keyboard", "price": 89.99, "quantity": 1}],
                "total_amount": 89.99,
                "status": "PENDING",
                "created_at": "2026-05-21T01:00:00Z",
                "updated_at": "2026-05-21T01:00:00Z"
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
                "created_at": "2026-05-21T02:00:00Z",
                "updated_at": "2026-05-21T02:00:00Z"
            }
        ])
        webhook_subscriptions.clear()
        event_log.clear()
        received_webhooks.clear()

    def test_root_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("Welcome", data["message"])

    def test_get_orders_filtering_and_sorting(self):
        # Filter by PENDING status
        response = self.client.get('/api/orders?status=PENDING')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["customer_name"], "Kha Anh")

        # Sort by total_amount ascending
        response = self.client.get('/api/orders?sort_by=total_amount&order=asc')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["items"][0]["id"], 2) # 89.97 is less than 89.99

    def test_get_orders_pagination_and_hateoas(self):
        response = self.client.get('/api/orders?page=1&limit=1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["pagination"]["total_items"], 2)
        self.assertEqual(data["pagination"]["total_pages"], 2)
        
        # Check HATEOAS collection links
        self.assertIn("self", data["_links"])
        self.assertIn("next", data["_links"])
        self.assertIn("create", data["_links"])

    def test_crud_lifecycle(self):
        # Create new order
        payload = {
            "customer_name": "Test User",
            "email": "test@example.com",
            "items": [{"name": "Desk Lamp", "price": 25.00, "quantity": 2}]
        }
        res = self.client.post('/api/orders', json=payload)
        self.assertEqual(res.status_code, 201)
        new_order = res.get_json()
        self.assertEqual(new_order["total_amount"], 50.00)
        self.assertEqual(new_order["status"], "PENDING")
        self.assertIn("pay", new_order["_links"])
        
        order_id = new_order["id"]

        # Read single
        res = self.client.get(f'/api/orders/{order_id}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["customer_name"], "Test User")

        # Update
        update_payload = {"customer_name": "Updated Test User"}
        res = self.client.put(f'/api/orders/{order_id}', json=update_payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["customer_name"], "Updated Test User")

        # Delete
        res = self.client.delete(f'/api/orders/{order_id}')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()["success"])

        # Confirm 404
        res = self.client.get(f'/api/orders/{order_id}')
        self.assertEqual(res.status_code, 404)

    def test_state_transitions_and_hateoas(self):
        # Order 1 is PENDING
        res = self.client.get('/api/orders/1')
        order = res.get_json()
        self.assertEqual(order["status"], "PENDING")
        self.assertIn("pay", order["_links"])
        self.assertIn("cancel", order["_links"])
        self.assertNotIn("ship", order["_links"])

        # Pay Order 1 -> transitions to PAID
        res = self.client.post('/api/orders/1/pay')
        self.assertEqual(res.status_code, 200)
        order = res.get_json()
        self.assertEqual(order["status"], "PAID")
        self.assertNotIn("pay", order["_links"])
        self.assertNotIn("cancel", order["_links"])
        self.assertIn("ship", order["_links"])

        # Ship Order 1 -> transitions to SHIPPED
        res = self.client.post('/api/orders/1/ship')
        self.assertEqual(res.status_code, 200)
        order = res.get_json()
        self.assertEqual(order["status"], "SHIPPED")
        self.assertNotIn("pay", order["_links"])
        self.assertNotIn("ship", order["_links"])

    def test_webhook_and_event_driven_dispatch(self):
        # 1. Register Webhook subscription
        webhook_payload = {
            "target_url": "http://127.0.0.1:8081",
            "events": ["order.created", "order.paid"]
        }
        res = self.client.post('/api/webhooks/subscriptions', json=webhook_payload)
        self.assertEqual(res.status_code, 201)
        sub = res.get_json()
        self.assertEqual(sub["target_url"], "http://127.0.0.1:8081")

        # 2. Trigger order.created event
        order_payload = {
            "customer_name": "Bob",
            "email": "bob@example.com",
            "items": [{"name": "Keycap Set", "price": 40.00, "quantity": 1}]
        }
        self.client.post('/api/orders', json=order_payload)

        # 3. Trigger order.paid event
        # The new order ID should be 3 (since database has 1 and 2, max + 1)
        self.client.post('/api/orders/3/pay')

        # 4. Trigger order.shipped event (not registered for webhooks, but in event_log)
        self.client.post('/api/orders/3/ship')

        # Give background thread a short moment to dispatch webhooks
        time.sleep(0.5)

        # 5. Assertions on Webhook Receiver
        self.assertEqual(len(received_webhooks), 2)
        self.assertEqual(received_webhooks[0]["event_type"], "order.created")
        self.assertEqual(received_webhooks[1]["event_type"], "order.paid")

        # 6. Assertions on Event Log
        res = self.client.get('/api/webhooks/events')
        events = res.get_json()
        self.assertEqual(len(events), 3) # order.created, order.paid, order.shipped
        self.assertEqual(events[0]["event_type"], "order.created")
        self.assertEqual(events[1]["event_type"], "order.paid")
        self.assertEqual(events[2]["event_type"], "order.shipped")

if __name__ == '__main__':
    unittest.main()
