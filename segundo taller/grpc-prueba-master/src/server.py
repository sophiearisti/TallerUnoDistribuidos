from concurrent import futures

import grpc

from constants import environment
from grpc_config import (
    client_pb2,
    client_pb2_grpc,
    op1_pb2,
    op1_pb2_grpc,
    op2_pb2,
    op2_pb2_grpc,
    op3_pb2,
    op3_pb2_grpc
)


class ServerHandler(client_pb2_grpc.ClientServicer):

    def RequestOperation(self, request, context):
        client_reply = client_pb2.ClientReply()
        # pedir primer cateto al cuadrado

        cateto1 = pedir_primer_cateto_cuadrado(request.cateto1)
        # pedir segundo cateto al cuadrado
        cateto2 = pedir_segundo_cateto_cuadrado(request.cateto2)
        # pedir hipotenusa
        hipotenusa = pedir_hipotenusa(request.cateto1, request.cateto2)
        # calcular hipotenusa
        client_reply.hipotenusa = hipotenusa

        return client_reply

#funcion grpc del op1
def pedir_primer_cateto_cuadrado(cateto: float) -> float:
    with grpc.insecure_channel(
        f"{environment.OP1_HOST}:{environment.OP1_PORT}"
    ) as channel:
        stub = op1_pb2_grpc.Op1Stub(channel)
        server_req = op1_pb2.Op1Request(cateto1=cateto)
        response = stub.Operation1(server_req)
        print(f"Response: {response.cateto1}")
        return response.cateto1 

#funcion grpc del op2
def pedir_segundo_cateto_cuadrado(cateto: float) -> float:
    with grpc.insecure_channel(
        f"{environment.OP2_HOST}:{environment.OP2_PORT}"
    ) as channel:
        stub = op2_pb2_grpc.Op2Stub(channel)
        server_req = op2_pb2.Op2Request(cateto2=cateto)
        response = stub.Operation2(server_req)
        print(f"Response: {response.cateto2}")
        return response.cateto2

#funcion grpc del op3
def pedir_hipotenusa(catetoA: float,catetoB: float) -> float:
    with grpc.insecure_channel(
        f"{environment.OP3_HOST}:{environment.OP3_PORT}"
    ) as channel:
        stub = op3_pb2_grpc.Op3Stub(channel)
        server_req = op3_pb2.Op3Request(cateto1=catetoA,cateto2=catetoB)
        response = stub.Operation3(server_req)
        print(f"Response: {response.hipotenusa}")
        return response.hipotenusa

def main() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_pb2_grpc.add_ClientServicer_to_server(ServerHandler(), server)
    server.add_insecure_port(f"[::]:{environment.SERVER_PORT}")  # constante del puerto
    print(f"Server running on port {environment.SERVER_PORT}  ")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
