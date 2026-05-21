import grpc

from grpc_demo import orders_pb2 as orders__pb2


class OrderServiceStub:
    def __init__(self, channel):
        self.ListOrders = channel.unary_unary(
            "/orders.OrderService/ListOrders",
            request_serializer=orders__pb2.ListOrdersRequest.SerializeToString,
            response_deserializer=orders__pb2.ListOrdersResponse.FromString,
        )
        self.GetOrder = channel.unary_unary(
            "/orders.OrderService/GetOrder",
            request_serializer=orders__pb2.OrderIdRequest.SerializeToString,
            response_deserializer=orders__pb2.OrderResponse.FromString,
        )
        self.CreateOrder = channel.unary_unary(
            "/orders.OrderService/CreateOrder",
            request_serializer=orders__pb2.CreateOrderRequest.SerializeToString,
            response_deserializer=orders__pb2.OrderResponse.FromString,
        )
        self.PayOrder = channel.unary_unary(
            "/orders.OrderService/PayOrder",
            request_serializer=orders__pb2.OrderIdRequest.SerializeToString,
            response_deserializer=orders__pb2.OrderResponse.FromString,
        )
        self.CancelOrder = channel.unary_unary(
            "/orders.OrderService/CancelOrder",
            request_serializer=orders__pb2.OrderIdRequest.SerializeToString,
            response_deserializer=orders__pb2.OrderResponse.FromString,
        )
        self.ShipOrder = channel.unary_unary(
            "/orders.OrderService/ShipOrder",
            request_serializer=orders__pb2.OrderIdRequest.SerializeToString,
            response_deserializer=orders__pb2.OrderResponse.FromString,
        )


class OrderServiceServicer:
    def ListOrders(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def GetOrder(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def CreateOrder(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def PayOrder(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def CancelOrder(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")

    def ShipOrder(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")


def add_OrderServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ListOrders": grpc.unary_unary_rpc_method_handler(
            servicer.ListOrders,
            request_deserializer=orders__pb2.ListOrdersRequest.FromString,
            response_serializer=orders__pb2.ListOrdersResponse.SerializeToString,
        ),
        "GetOrder": grpc.unary_unary_rpc_method_handler(
            servicer.GetOrder,
            request_deserializer=orders__pb2.OrderIdRequest.FromString,
            response_serializer=orders__pb2.OrderResponse.SerializeToString,
        ),
        "CreateOrder": grpc.unary_unary_rpc_method_handler(
            servicer.CreateOrder,
            request_deserializer=orders__pb2.CreateOrderRequest.FromString,
            response_serializer=orders__pb2.OrderResponse.SerializeToString,
        ),
        "PayOrder": grpc.unary_unary_rpc_method_handler(
            servicer.PayOrder,
            request_deserializer=orders__pb2.OrderIdRequest.FromString,
            response_serializer=orders__pb2.OrderResponse.SerializeToString,
        ),
        "CancelOrder": grpc.unary_unary_rpc_method_handler(
            servicer.CancelOrder,
            request_deserializer=orders__pb2.OrderIdRequest.FromString,
            response_serializer=orders__pb2.OrderResponse.SerializeToString,
        ),
        "ShipOrder": grpc.unary_unary_rpc_method_handler(
            servicer.ShipOrder,
            request_deserializer=orders__pb2.OrderIdRequest.FromString,
            response_serializer=orders__pb2.OrderResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("orders.OrderService", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
