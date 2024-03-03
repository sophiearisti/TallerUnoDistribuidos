from concurrent import futures

import grpc

from constants import environment
from grpc_config import op2_pb2, op2_pb2_grpc


class OP2Handler(op2_pb2_grpc.Op2Servicer):

    def Operation2(self, request, context):
        op2_reply = op2_pb2.Op2Reply()
        print(f"Operacion recibida, valor del cateto: {request.cateto2}")
        op2_reply.cateto2 = request.cateto2**2
        print(f"Respuesta a enviar {request.cateto2**2}")
        return op2_reply


def main() -> None:
    op2 = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    op2_pb2_grpc.add_Op2Servicer_to_server(OP2Handler(), op2)
    op2.add_insecure_port(f"[::]:{environment.OP2_PORT}")  # constante del puerto
    print(f"Server running on port {environment.OP2_PORT}")
    op2.start()
    op2.wait_for_termination()


if __name__ == "__main__":
    main()
