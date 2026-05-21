# Week 11-12: Advanced API Design Patterns

This directory contains a complete, lightweight, pure-backend demonstration API built using Python and Flask. It combines multiple advanced API design patterns: **CRUD**, **Query Pattern**, **HATEOAS**, **Event-Driven Architecture (EDA)**, and **Webhooks**.

---

## 📖 Architecture & Design Patterns

### 1. CRUD (Create, Read, Update, Delete)
The basic lifecycle of an Order resource is handled using standard HTTP methods maps:
- `POST /api/orders` (Create)
- `GET /api/orders` (Read collection)
- `GET /api/orders/<id>` (Read single)
- `PUT /api/orders/<id>` (Update)
- `DELETE /api/orders/<id>` (Delete)

### 2. Query Pattern
Provides robust capabilities to filter, sort, and paginate large collections:
- **Filtering**: Filter orders by `status`, `customer` (fuzzy search), and `min_amount` (price threshold).
- **Sorting**: Sort by fields (`id`, `customer_name`, `total_amount`, `created_at`, `updated_at`) with ascending/descending order control.
- **Pagination**: Client-driven pagination using `page` and `limit` parameters, returning metadata such as `total_items` and `total_pages`.

### 3. HATEOAS (Hypermedia As The Engine Of Application State)
Rather than hardcoding route URIs on the client-side, the API response informs the client of the actions available based on the resource's current state:
- Each order contains a `_links` object showing transitions like `self` (GET), `update` (PUT), and `delete` (DELETE).
- State-specific links are added dynamically:
  - If status is `PENDING`, links to `pay` (POST) and `cancel` (POST) are provided.
  - If status is `PAID`, a link to `ship` (POST) is provided.
- The collection list returns hypermedia pagination links (`self`, `next`, `prev`).

### 4. Event-Driven Architecture (EDA) & Webhooks
State changes inside the Order microservice emit asynchronous domain events:
- **Event Log**: Every state transition publishes an event to an in-memory event logger (available at `GET /api/webhooks/events`).
- **Webhook Subscriptions**: Clients register a target URL and list of event types (or `*` for all) via `POST /api/webhooks/subscriptions`.
- **Asynchronous Dispatching**: Upon event firing, the server invokes webhooks asynchronously using background threads to ensure non-blocking HTTP responses for API requests.

---

## ⚡ REST vs. gRPC vs. GraphQL: Comparison & Guidelines

This section helps you understand when to choose which architectural style or technology.

| Feature | REST (Representational State Transfer) | gRPC (Google Remote Procedure Call) | GraphQL |
| :--- | :--- | :--- | :--- |
| **Protocol / Transport** | HTTP/1.1 (standard) or HTTP/2 | HTTP/2 (strictly required) | HTTP/1.1 or HTTP/2 |
| **Data Format** | Typically JSON, XML, or Form Data | Protocol Buffers (Binary) | JSON |
| **Schema & Typing** | Optional (OpenAPI/Swagger) | Strict (defined in `.proto` files) | Strict (defined in GraphQL Schema SDL) |
| **API Paradigm** | Resource-oriented (noun-based URLs) | Procedure-oriented (RPC methods) | Graph-oriented (Single query endpoint) |
| **Network Overhead** | Medium-High (text-based JSON, headers) | Low (compressed binary format) | Medium (negotiable payload sizes) |
| **Streaming** | Server-Sent Events (SSE), WebSockets | Bi-directional streaming native | Subscriptions (typically over WebSockets) |
| **Over- / Under-fetching** | Common (returns full resource) | Common (returns defined message structs) | Solved (clients query exactly what they need) |

### When to use REST
- **Public & Third-Party APIs**: REST is the industry standard with universal browser support and simple tools (`curl`, Postman, etc.).
- **Simple CRUD Apps**: Ideal when systems map directly to database resources.
- **Resource Caching**: Highly effective because it utilizes standard HTTP caching headers and methods (`GET`).

### When to use gRPC
- **Microservices Communication (East-West traffic)**: Fast serialization, low CPU usage, and multiplexed HTTP/2 streams make gRPC the perfect choice for internal service-to-service calls.
- **Polyglot Environments**: gRPC automatically generates typed client/server stubs in Python, Go, Java, Node.js, C#, etc. from the same `.proto` schema.
- **Real-Time Streaming**: Native support for client-side, server-side, and bidirectional streaming (e.g. log ingestion, chat apps, live feeds).

### When to use GraphQL
- **Complex UI Dashboards**: Perfect when client applications need to aggregate data from multiple entities in a single request (e.g. User + Orders + Notifications + Profile Settings).
- **Bandwidth-constrained Clients (Mobile/IoT)**: The client specifies only the needed fields, eliminating over-fetching and saving mobile data.
- **Rapidly Evolving Frontends**: Frontend developers can modify query fields without needing backend team support or API version changes.

---

## 🚀 Running the demos

Install dependencies once:

```bash
cd Week11-12
pip install -r requirements.txt
```

This week now has three API styles side by side over the same **Order** domain:

| Style | Main file | Port | Best for |
| :--- | :--- | :--- | :--- |
| REST | `app.py` | `8000` | Resource CRUD, HATEOAS, webhooks |
| GraphQL | `graphql_app.py` | `8001` | Client-selected fields and nested reads |
| gRPC | `grpc_demo/server.py` | `50051` | Fast typed service-to-service calls |

### REST API

```bash
python app.py
```

The REST server runs locally on `http://localhost:8000`.

### GraphQL API

```bash
python graphql_app.py
```

The GraphQL server runs locally on `http://localhost:8001/graphql`.

### gRPC API

Start the gRPC server:

```bash
python -m grpc_demo.server
```

In another terminal, run the sample client:

```bash
python -m grpc_demo.client
```

The gRPC service listens on `127.0.0.1:50051`.

---

## 🧪 Testing Walkthrough (Pure Backend)

### 1. Webhook Registration (Optional)
To test webhooks locally, you can spin up a listener (e.g., using a service like Webhook.site or writing a tiny Flask app that prints requests).
Alternatively, you can test registering a webhook with any target URL:

```bash
curl -X POST http://localhost:8000/api/webhooks/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://httpbin.org/post",
    "events": ["order.created", "order.paid"]
  }'
```

### 2. Querying Orders (Pagination, Filtering, Sorting)
Retrieve orders with Query Patterns applied:
```bash
curl "http://localhost:8000/api/orders?status=PENDING&sort_by=total_amount&order=desc"
```

### 3. Placing an Order (Creates Event `order.created`)
Create a new order:
```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Nguyen Van A",
    "email": "vana@example.com",
    "items": [
      {"name": "Mechanical Keyboard", "price": 99.00, "quantity": 1},
      {"name": "USB-C Hub", "price": 25.50, "quantity": 2}
    ]
  }'
```
*Observe that the response contains `_links` allowing you to perform state actions (`pay`, `cancel`) because status is `PENDING`.*

### 4. Transition State (Triggers Event `order.paid`)
Invoke the HATEOAS action path returned in the previous response to pay for the order (e.g., for Order ID 3):
```bash
curl -X POST http://localhost:8000/api/orders/3/pay
```
*Note that the status transitions to `PAID`, the webhook triggers, and the HATEOAS actions list updates, replacing `pay`/`cancel` with a `ship` action.*

### 5. Inspecting Fired Events
Check the in-memory event registry to confirm events were successfully emitted and logged:
```bash
curl http://localhost:8000/api/webhooks/events
```

---

## 🧪 GraphQL quick test

Query only the fields the client needs:

```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ orders(status: \"PENDING\") { items { id customerName status totalAmount } totalItems } }"
  }'
```

Create an order with a mutation:

```bash
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CreateOrder($input: CreateOrderInput!) { createOrder(input: $input) { id customerName status totalAmount } }",
    "variables": {
      "input": {
        "customerName": "Nguyen Van A",
        "email": "vana@example.com",
        "items": [
          {"name": "USB-C Hub", "price": 25.5, "quantity": 2},
          {"name": "Notebook Stand", "price": 39.0, "quantity": 1}
        ]
      }
    }
  }'
```

---

## 🧪 gRPC quick test

Run the server:

```bash
python -m grpc_demo.server
```

Run the client from a second terminal:

```bash
python -m grpc_demo.client
```

The client demonstrates:
- `ListOrders`
- `CreateOrder`
- `PayOrder`
- `GetOrder`

The service contract is defined in `grpc_demo/orders.proto`.
