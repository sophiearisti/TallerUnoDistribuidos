from concurrent import futures

import grpc

from constants import environment
from grpc_config import op3_pb2, op3_pb2_grpc


class OP3Handler(op3_pb2_grpc.Op3Servicer):

    def Operation1(self, request, context):
        op3_reply = op3_pb2.Op3Reply()

        op3_reply.hipotenusa = pow(request.cateto1 + request.cateto2,0.5)

        return op3_reply


def main() -> None:
    op3 = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    op3_pb2_grpc.add_Op3Servicer_to_server(OP3Handler(), op3)
    op3.add_insecure_port(f"[::]:{environment.OP3_PORT}")  # constante del puerto
    print(f"Server running on port {environment.OP3_PORT}")
    op3.start()
    op3.wait_for_termination()


if __name__ == "__main__":
    main()
