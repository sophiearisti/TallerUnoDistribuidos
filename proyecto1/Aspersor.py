import zmq


encendido=false


def main():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.bind(f"tcp://{self.ip_propia}:5558")
    while True:
        print("RECIBIENDO MENSAJES...")


if __name__ == "__main__":
    main()