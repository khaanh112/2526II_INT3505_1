from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder


_sym_db = _symbol_database.Default()


def _add_field(message, name, number, field_type, label=None, type_name=None):
    field = message.field.add()
    field.name = name
    field.number = number
    field.label = label or _descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field.type = field_type
    if type_name:
        field.type_name = type_name


file_proto = _descriptor_pb2.FileDescriptorProto()
file_proto.name = "grpc_demo/orders.proto"
file_proto.package = "orders"
file_proto.syntax = "proto3"

order_item = file_proto.message_type.add()
order_item.name = "OrderItem"
_add_field(order_item, "name", 1, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(order_item, "price", 2, _descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE)
_add_field(order_item, "quantity", 3, _descriptor_pb2.FieldDescriptorProto.TYPE_INT32)

order = file_proto.message_type.add()
order.name = "Order"
_add_field(order, "id", 1, _descriptor_pb2.FieldDescriptorProto.TYPE_INT32)
_add_field(order, "customer_name", 2, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(order, "email", 3, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(
    order,
    "items",
    4,
    _descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE,
    label=_descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED,
    type_name=".orders.OrderItem",
)
_add_field(order, "total_amount", 5, _descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE)
_add_field(order, "status", 6, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(order, "created_at", 7, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(order, "updated_at", 8, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)

list_request = file_proto.message_type.add()
list_request.name = "ListOrdersRequest"
_add_field(list_request, "status", 1, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(list_request, "customer", 2, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(list_request, "min_amount", 3, _descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE)
_add_field(list_request, "page", 4, _descriptor_pb2.FieldDescriptorProto.TYPE_INT32)
_add_field(list_request, "limit", 5, _descriptor_pb2.FieldDescriptorProto.TYPE_INT32)
_add_field(list_request, "sort_by", 6, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(list_request, "order", 7, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)

list_response = file_proto.message_type.add()
list_response.name = "ListOrdersResponse"
_add_field(
    list_response,
    "items",
    1,
    _descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE,
    label=_descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED,
    type_name=".orders.Order",
)
_add_field(list_response, "page", 2, _descriptor_pb2.FieldDescriptorProto.TYPE_INT32)
_add_field(list_response, "limit", 3, _descriptor_pb2.FieldDescriptorProto.TYPE_INT32)
_add_field(list_response, "total_items", 4, _descriptor_pb2.FieldDescriptorProto.TYPE_INT32)
_add_field(list_response, "total_pages", 5, _descriptor_pb2.FieldDescriptorProto.TYPE_INT32)

id_request = file_proto.message_type.add()
id_request.name = "OrderIdRequest"
_add_field(id_request, "id", 1, _descriptor_pb2.FieldDescriptorProto.TYPE_INT32)

create_request = file_proto.message_type.add()
create_request.name = "CreateOrderRequest"
_add_field(create_request, "customer_name", 1, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(create_request, "email", 2, _descriptor_pb2.FieldDescriptorProto.TYPE_STRING)
_add_field(
    create_request,
    "items",
    3,
    _descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE,
    label=_descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED,
    type_name=".orders.OrderItem",
)

order_response = file_proto.message_type.add()
order_response.name = "OrderResponse"
_add_field(
    order_response,
    "order",
    1,
    _descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE,
    type_name=".orders.Order",
)

service = file_proto.service.add()
service.name = "OrderService"
for name, input_type, output_type in [
    ("ListOrders", ".orders.ListOrdersRequest", ".orders.ListOrdersResponse"),
    ("GetOrder", ".orders.OrderIdRequest", ".orders.OrderResponse"),
    ("CreateOrder", ".orders.CreateOrderRequest", ".orders.OrderResponse"),
    ("PayOrder", ".orders.OrderIdRequest", ".orders.OrderResponse"),
    ("CancelOrder", ".orders.OrderIdRequest", ".orders.OrderResponse"),
    ("ShipOrder", ".orders.OrderIdRequest", ".orders.OrderResponse"),
]:
    method = service.method.add()
    method.name = name
    method.input_type = input_type
    method.output_type = output_type

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(file_proto.SerializeToString())
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "grpc_demo.orders_pb2", globals())
