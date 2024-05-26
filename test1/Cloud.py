import threading
import zmq
import json
import pymongo
from pymongo import MongoClient
from datetime import datetime
from constants import environment
import time
from scalene import scalene_profiler

class Cloud:
    context = zmq.Context()
    senderSC = context.socket(zmq.REQ)

    def __init__(self):
        self.client = MongoClient(environment.MONGODB['uri'], tlsAllowInvalidCertificates=True)
        self.db = self.client[environment.MONGODB['database']]
        self.collection = self.db[environment.MONGODB['collection_sensor']]
        self.collection_temperatura= self.db[environment.MONGODB['collection_calc']]
        self.collection_alerta= self.db[environment.MONGODB['collection_alerta']]
    
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
        if(informacion["tipo_mensaje"]=="Alerta"):
            informacion["TS"] = datetime.fromtimestamp(informacion["TS"])
            self.collection_alerta.insert_one(informacion)
        elif(informacion["tipo_mensaje"]=="Temperatura"):
            informacion["TS"] = datetime.fromtimestamp(informacion["TS"])
            self.collection_temperatura.insert_one(informacion)
        elif(informacion["tipo_mensaje"]=="Humedad"):
            info2=informacion
            informacion["TS"] = datetime.fromtimestamp(informacion["TS"])
            self.collection_temperatura.insert_one(informacion)
            self.sumarHumedades(info2)
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
            result["TS"] = datetime.fromtimestamp(result["TS"])
            self.collection_temperatura.insert_one(result)

            if(valor>environment.MAX_HUMEDAD):
                alerta = {
                    "tipo_mensaje": "Alerta",
                    "valor": valor,
                    "TS": timestamp,
                }
                self.collection_alerta.insert_one(alerta)
                self.senderSC.connect(
                f"tcp://{environment.SC_CLOUD['host']}:{environment.SC_CLOUD['port']}"
                 )
                msg = f"Alarma promedio humedad: {valor} por encima del valor maximo"
                self.senderSC.send_string(msg)
                msg_in = self.senderSC.recv_string()
                print(msg_in)

                

    sumatoriahumedad=0
    def sumarHumedades(self,result):
       self.sumatoriahumedad+=result['valor']
        
def main():
    cloud = Cloud()
    cloud.inicializar()

if __name__ == "__main__":
   scalene_profiler.start()
   main()
