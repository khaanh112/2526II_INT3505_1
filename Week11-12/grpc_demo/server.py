import os
import sys
from concurrent import futures

import grpc

CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import order_store
from grpc_demo import orders_pb2, orders_pb2_grpc


def order_item_to_proto(item):
    return orders_pb2.OrderItem(
        name=item["name"],
        price=item["price"],
        quantity=item["quantity"],
    )


def order_to_proto(order):
    return orders_pb2.Order(
        id=order["id"],
        customer_name=order["customer_name"],
        email=order["email"],
        items=[order_item_to_proto(item) for item in order["items"]],
        total_amount=order["total_amount"],
        status=order["status"],
        created_at=order["created_at"],
        updated_at=order["updated_at"],
    )


class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def ListOrders(self, request, context):
        min_amount = request.min_amount if request.min_amount > 0 else None
        result = order_store.list_orders(
            status=request.status or None,
            customer=request.customer or None,
            min_amount=min_amount,
            page=request.page or 1,
            limit=request.limit or 5,
            sort_by=request.sort_by or "created_at",
            sort_order=request.order or "desc",
        )

        return orders_pb2.ListOrdersResponse(
            items=[order_to_proto(order) for order in result["items"]],
            page=result["page"],
            limit=result["limit"],
            total_items=result["total_items"],
            total_pages=result["total_pages"],
        )

    def GetOrder(self, request, context):
        try:
            order = order_store.get_order(request.id)
        except order_store.OrderNotFound as exc:
            context.abort(grpc.StatusCode.NOT_FOUND, str(exc))
        return orders_pb2.OrderResponse(order=order_to_proto(order))

    def CreateOrder(self, request, context):
        items = [
            {"name": item.name, "price": item.price, "quantity": item.quantity}
            for item in request.items
        ]
        try:
            order = order_store.create_order(request.customer_name, request.email, items)
        except order_store.ValidationError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        return orders_pb2.OrderResponse(order=order_to_proto(order))

    def PayOrder(self, request, context):
        return self._transition(request.id, "pay", context)

    def CancelOrder(self, request, context):
        return self._transition(request.id, "cancel", context)

    def ShipOrder(self, request, context):
        return self._transition(request.id, "ship", context)

    def _transition(self, order_id, action, context):
        try:
            order = order_store.transition_order(order_id, action)
        except order_store.OrderNotFound as exc:
            context.abort(grpc.StatusCode.NOT_FOUND, str(exc))
        except order_store.InvalidState as exc:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(exc))
        except order_store.ValidationError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        return orders_pb2.OrderResponse(order=order_to_proto(order))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port("127.0.0.1:50051")
    server.start()
    print("gRPC OrderService is running on 127.0.0.1:50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
