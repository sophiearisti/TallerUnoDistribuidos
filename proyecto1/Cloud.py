import threading
import zmq
import json
import pymongo
from pymongo import MongoClient
from datetime import datetime
from constants import environment
import time

class Cloud:
    context = zmq.Context()

    def __init__(self):
        self.client = MongoClient(environment.MONGODB['uri'], tlsAllowInvalidCertificates=True)
        self.db = self.client[environment.MONGODB['database']]
        self.collection = self.db[environment.MONGODB['collection_sensor']]
        self.collection_temperatura= self.db[environment.MONGODB['collection_calc']]
    
    def inicializar(self):
        receiver = self.context.socket(zmq.REP)
        receiver.bind(f"tcp://{environment.CLOUD['host']}:{environment.CLOUD['port']}")
        
        print("RECIBIENDO MENSAJES...")
        threading.Thread(target=self.calcularHumedadGeneral).start()

        while True:
            result = receiver.recv_json()
            print(f"mensaje recibido {result}")
            receiver.send_string("Mensaje recibido CLOUD")
            self.enviar_BDD(result)


    def enviar_BDD(self, informacion):
        print("ENVIAR A BDD")
        if(informacion["tipo_mensaje"]=="Temperatura"):
            self.collection_temperatura.insert_one(informacion)
        elif(informacion["tipo_mensaje"]=="Humedad"):
            self.collection_temperatura.insert_one(informacion)
            self.sumarHumedades(informacion)
        else:
            self.collection.insert_one(informacion)

    def calcularHumedadGeneral(self):
        while True:
            time.sleep(20)
            valor = self.sumatoriahumedad / environment.CANT_SENSORES
            timestamp = time.time()
            result = {
                "tipo_mensaje": "Humedad_general",
                "valor": valor,
                "TS": timestamp,
            }
            print("humedad general {result}")
            self.collection_temperatura.insert_one(result)

    sumatoriahumedad=0
    def sumarHumedades(self,result):
       self.sumatoriahumedad+=result['valor']
        
def main():
    cloud = Cloud()
    cloud.inicializar()

if __name__ == "__main__":
   main()
