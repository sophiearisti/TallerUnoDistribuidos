
import zmq
import json
from datetime import datetime
from constants import environment

class Cloud:
    context = zmq.Context()

    def inicializar(self):
        receiver = self.context.socket(zmq.REP)
        receiver.bind(f"tcp://{environment.CLOUD['host']}:{environment.CLOUD['port']}")
        print("RECIBIENDO MENSAJES...")
        while True:
            result = receiver.recv_json()
            print(f"mensaje recibido {result}")
            receiver.send("Mensaje recibido")

    def enviar_BDD(self, informacion):
        print("ENVIAR A BDD")



def main():
    cloud = Cloud()
    cloud.inicializar()

if __name__ == "__main__":
   main()