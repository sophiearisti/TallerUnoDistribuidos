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
    #INICIALIZAR LOS STUBS DE CADA PETICION
    def __init__(self):
        self.channel_op1 = grpc.insecure_channel(f"{environment.OP1_HOST}:{environment.OP1_PORT}")
        self.stub_op1 = op1_pb2_grpc.Op1Stub(self.channel_op1)

        self.channel_op2 = grpc.insecure_channel(f"{environment.OP2_HOST}:{environment.OP2_PORT}")
        self.stub_op2 = op2_pb2_grpc.Op2Stub(self.channel_op2)

        self.channel_op3 = grpc.insecure_channel(f"{environment.OP3_HOST}:{environment.OP3_PORT}")
        self.stub_op3 = op3_pb2_grpc.Op3Stub(self.channel_op3)

    def RequestOperation(self, request, context):
        respuesta = client_pb2.ClientReply()

        # OP1 - pedir primer cateto al cuadrado
        print(f"[Peticion] Server OP1 cateto: {request.cateto1}")
        cateto1 = self.obtener_cateto1(request.cateto1)
        
        # OP2 - pedir segundo cateto al cuadrado
        print(f"[Peticion] Server OP2 cateto: {request.cateto2}")
        cateto2 = self.obtener_cateto2(request.cateto2)

        # OP3 - pedir hipotenusa
        print(f"[Peticion] Server OP3 catetos: (catetoA: {cateto1} catetoB: {cateto2})")
        hipotenusa = self.obtener_hipotenusa(cateto1, cateto2)

        respuesta.hipotenusa = hipotenusa
        return respuesta

    def obtener_cateto1(self, cateto):
        try:
            response = self.stub_op1.Operation1(op1_pb2.Op1Request(cateto1=cateto))
            print(f"[Response] OP1: {response.cateto1}")
            return response.cateto1
        except grpc.RpcError as err:
            print(f"[Error] {err}")
            return pow(cateto, 2)

    def obtener_cateto2(self, cateto):
        try:
            response = self.stub_op2.Operation2(op2_pb2.Op2Request(cateto2=cateto))
            print(f"[Respuestta] OP2: {response.cateto2}")
            return response.cateto2
        except grpc.RpcError as err:
            print(f"[Error] {err}")
            return pow(cateto, 2)

    def obtener_hipotenusa(self, cateto1, cateto2):
        try:
            response = self.stub_op3.Operation3(op3_pb2.Op3Request(cateto1=cateto1, cateto2=cateto2))
            print(f"[Respuesta] OP3: {response.hipotenusa}")
            return response.hipotenusa
        except grpc.RpcError as err:
            print(f"[Error] {err}")
            return pow(cateto1 + cateto2, 0.5)

def main() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_pb2_grpc.add_ClientServicer_to_server(ServerHandler(), server)
    server.add_insecure_port(f"[::]:{environment.SERVER_PORT}")  # constante del puerto
    print(f"Servidor corriendo en puerto {environment.SERVER_PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    main()