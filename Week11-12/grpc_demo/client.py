import grpc
from google.protobuf.json_format import MessageToDict

from grpc_demo import orders_pb2, orders_pb2_grpc


def print_response(title, message):
    print(f"\n{title}")
    print(MessageToDict(message, preserving_proto_field_name=True))


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = orders_pb2_grpc.OrderServiceStub(channel)

        order_list = stub.ListOrders(
            orders_pb2.ListOrdersRequest(status="PENDING", page=1, limit=5)
        )
        print_response("1. List pending orders", order_list)

        created = stub.CreateOrder(
            orders_pb2.CreateOrderRequest(
                customer_name="Nguyen Van A",
                email="vana@example.com",
                items=[
                    orders_pb2.OrderItem(name="USB-C Hub", price=25.5, quantity=2),
                    orders_pb2.OrderItem(name="Notebook Stand", price=39.0, quantity=1),
                ],
            )
        )
        print_response("2. Create order", created)

        order_id = created.order.id
        paid = stub.PayOrder(orders_pb2.OrderIdRequest(id=order_id))
        print_response("3. Pay order", paid)

        loaded = stub.GetOrder(orders_pb2.OrderIdRequest(id=order_id))
        print_response("4. Get order by id", loaded)


if __name__ == "__main__":
    main()
