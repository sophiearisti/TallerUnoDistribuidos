import zmq
import json
import pymongo
from pymongo import MongoClient
from datetime import datetime
from constants import environment

class Cloud:
    context = zmq.Context()

    def __init__(self):
        self.client = MongoClient(environment.MONGODB['uri'])
        self.db = self.client[environment.MONGODB['database']]
        self.collection = self.db[environment.MONGODB['collection_sensor']]
    
    def inicializar(self):
        receiver = self.context.socket(zmq.REP)
        receiver.bind(f"tcp://{environment.CLOUD['host']}:{environment.CLOUD['port']}")
        print("RECIBIENDO MENSAJES...")
        while True:
            result = receiver.recv_json()
            print(f"mensaje recibido {result}")
            receiver.send_string("Mensaje recibido")
            self.enviar_BDD(result)

    def enviar_BDD(self, informacion):
        print("ENVIAR A BDD")
        self.collection.insert_one(informacion)
        
def main():
    cloud = Cloud()
    cloud.inicializar()

if __name__ == "__main__":
   main()
