import grpc

from constants import environment
from grpc_config import client_pb2, client_pb2_grpc


def pedir_catetos() -> tuple[float, float]:
    cateto_a = float(input("Ingrese el valor del cateto a: "))
    cateto_b = float(input("Ingrese el valor del cateto b: "))
    return cateto_a, cateto_b


def main() -> None:
    with grpc.insecure_channel(
        f"{environment.SERVER_HOST}:{environment.SERVER_PORT}"
    ) as channel:
        c1, c2 = pedir_catetos()
        stub = client_pb2_grpc.ClientStub(channel)
        client_req = client_pb2.ClientRequest(cateto1=c1, cateto2=c2)
        response = stub.RequestOperation(client_req)
        print(f"Response: {response.hipotenusa}")


if __name__ == "__main__":
    main()
