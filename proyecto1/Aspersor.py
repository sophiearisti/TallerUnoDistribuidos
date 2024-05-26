import zmq

from constants import environment


def main():
    context = zmq.Context()
    receiver = context.socket(zmq.REP)
    receiver.bind(
        f"tcp://{environment.ASPERSOR['host']}:{environment.ASPERSOR['port']}"
    )
    print("RECIBIENDO MENSAJES...")

    while True:
        result = receiver.recv_string()
        print("ASPERSOR ACTIVADO")
        print(f"mensaje recibido {result}")
        receiver.send_string("Mensaje recibido por el ASPERSOR")


if __name__ == "__main__":
    main()
