from flask import Flask, jsonify, request
from graphql import build_schema, graphql_sync

import order_store


schema = build_schema(
    """
    type OrderItem {
      name: String!
      price: Float!
      quantity: Int!
    }

    type Order {
      id: Int!
      customerName: String!
      email: String!
      items: [OrderItem!]!
      totalAmount: Float!
      status: String!
      createdAt: String!
      updatedAt: String!
    }

    type OrderPage {
      items: [Order!]!
      page: Int!
      limit: Int!
      totalItems: Int!
      totalPages: Int!
    }

    type Event {
      id: Int!
      eventType: String!
      timestamp: String!
      data: Order!
    }

    input OrderItemInput {
      name: String!
      price: Float!
      quantity: Int = 1
    }

    input CreateOrderInput {
      customerName: String!
      email: String!
      items: [OrderItemInput!]!
    }

    type Query {
      orders(
        status: String
        customer: String
        minAmount: Float
        page: Int = 1
        limit: Int = 5
        sortBy: String = "created_at"
        order: String = "desc"
      ): OrderPage!
      order(id: Int!): Order
      events: [Event!]!
    }

    type Mutation {
      createOrder(input: CreateOrderInput!): Order!
      payOrder(id: Int!): Order!
      cancelOrder(id: Int!): Order!
      shipOrder(id: Int!): Order!
    }
    """
)


def resolve_orders(_root, _info, status=None, customer=None, minAmount=None, page=1, limit=5, sortBy="created_at", order="desc"):
    return order_store.list_orders(
        status=status,
        customer=customer,
        min_amount=minAmount,
        page=page,
        limit=limit,
        sort_by=sortBy,
        sort_order=order,
    )


def resolve_order(_root, _info, id):
    try:
        return order_store.get_order(id)
    except order_store.OrderNotFound:
        return None


def resolve_create_order(_root, _info, input):
    items = [
        {
            "name": item["name"],
            "price": item["price"],
            "quantity": item.get("quantity", 1),
        }
        for item in input["items"]
    ]
    return order_store.create_order(input["customerName"], input["email"], items)


def resolve_pay_order(_root, _info, id):
    return order_store.transition_order(id, "pay")


def resolve_cancel_order(_root, _info, id):
    return order_store.transition_order(id, "cancel")


def resolve_ship_order(_root, _info, id):
    return order_store.transition_order(id, "ship")


def resolve_events(_root, _info):
    return order_store.list_events()


def map_dict_field(source_key):
    return lambda source, _info: source[source_key]


schema.type_map["Query"].fields["orders"].resolve = resolve_orders
schema.type_map["Query"].fields["order"].resolve = resolve_order
schema.type_map["Query"].fields["events"].resolve = resolve_events
schema.type_map["Mutation"].fields["createOrder"].resolve = resolve_create_order
schema.type_map["Mutation"].fields["payOrder"].resolve = resolve_pay_order
schema.type_map["Mutation"].fields["cancelOrder"].resolve = resolve_cancel_order
schema.type_map["Mutation"].fields["shipOrder"].resolve = resolve_ship_order

schema.type_map["Order"].fields["customerName"].resolve = map_dict_field("customer_name")
schema.type_map["Order"].fields["totalAmount"].resolve = map_dict_field("total_amount")
schema.type_map["Order"].fields["createdAt"].resolve = map_dict_field("created_at")
schema.type_map["Order"].fields["updatedAt"].resolve = map_dict_field("updated_at")
schema.type_map["OrderPage"].fields["totalItems"].resolve = map_dict_field("total_items")
schema.type_map["OrderPage"].fields["totalPages"].resolve = map_dict_field("total_pages")
schema.type_map["Event"].fields["eventType"].resolve = map_dict_field("event_type")


app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(
        {
            "message": "GraphQL Order API demo",
            "endpoint": "/graphql",
            "example_query": "{ orders { items { id customerName status totalAmount } totalItems } }",
        }
    )


@app.route("/graphql", methods=["POST"])
def graphql_endpoint():
    payload = request.get_json(silent=True) or {}
    query = payload.get("query")

    if not query:
        return jsonify({"errors": [{"message": "Field 'query' is required"}]}), 400

    result = graphql_sync(
        schema,
        query,
        variable_values=payload.get("variables"),
        operation_name=payload.get("operationName"),
    )

    response = {}
    if result.errors:
        response["errors"] = [{"message": error.message} for error in result.errors]
    if result.data is not None:
        response["data"] = result.data

    status_code = 400 if result.errors and result.data is None else 200
    return jsonify(response), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
