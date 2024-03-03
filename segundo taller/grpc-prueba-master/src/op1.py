from concurrent import futures

import grpc

from constants import environment
from grpc_config import op1_pb2, op1_pb2_grpc


class OP1Handler(op1_pb2_grpc.Op1Servicer):

    def Operation1(self, request, context):
        op1_reply = op1_pb2.Op1Reply()

        op1_reply.cateto1 = request.cateto1**2

        return op1_reply


def main() -> None:
    op1 = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    op1_pb2_grpc.add_Op1Servicer_to_server(OP1Handler(), op1)
    op1.add_insecure_port(f"[::]:{environment.OP1_PORT}")  # constante del puerto
    print(f"Server running on port {environment.OP1_PORT}")
    op1.start()
    op1.wait_for_termination()


if __name__ == "__main__":
    main()
