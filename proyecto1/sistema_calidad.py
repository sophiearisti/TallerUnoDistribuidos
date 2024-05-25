import zmq
import argparse
from constants import environment

def main(param):
    if param not in [1, 2, 3]:
        print("Error: El parámetro debe ser un número entre 1 y 3.")
        return

    context = zmq.Context()
    receiver = context.socket(zmq.REP)
    if param==1:
        receiver.bind(f"tcp://{environment.SC_EDGE['host']}:{environment.SC_EDGE['port']}")
    elif param==2:
        receiver.bind(f"tcp://{environment.SC_FOG['host']}:{environment.SC_FOG['port']}")
    else:
        receiver.bind(f"tcp://{environment.SC_CLOUD['host']}:{environment.SC_CLOUD['port']}")

    print("RECIBIENDO MENSAJES...")

    while True:
        result = receiver.recv()
        print("ALARMA RECIBIDA")
        print(result)
        receiver.send(b"Mensaje recibido por el SC")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Procesa un parámetro del 1 al 3.')
    parser.add_argument('param', type=int, help='Un número entre 1 y 3')

    args = parser.parse_args()

    main(args.param)
