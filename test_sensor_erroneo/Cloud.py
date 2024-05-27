import json
import signal
import threading
import time
from datetime import datetime

import pymongo
import zmq
from pymongo import MongoClient

from constants import environment


class Cloud:
    context = zmq.Context()
    senderSC = context.socket(zmq.REQ)

    def __init__(self):
        self.client = MongoClient(
            environment.MONGODB["uri"], tlsAllowInvalidCertificates=True
        )
        self.db = self.client[environment.MONGODB["database"]]
        self.collection = self.db[environment.MONGODB["collection_sensor"]]
        self.collection_temperatura = self.db[environment.MONGODB["collection_calc"]]
        self.collection_alerta = self.db[environment.MONGODB["collection_alerta"]]
        self.collection_time = self.db[environment.MONGODB["collection_time"]]
        self.sumatoriahumedad = 0

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
        # Obtener el timestamp actual
        timestamp_actual = datetime.timestamp(datetime.now())
        # Restar el timestamp almacenado en informacion["TS"] al timestamp actual
        diferencia_tiempo = timestamp_actual - informacion["TS_FOG"]
        result = {
                "demora": diferencia_tiempo,
        }
        self.collection_time.insert_one(result)
        if informacion["tipo_mensaje"] == "Alerta":
            informacion["TS"] = datetime.fromtimestamp(informacion["TS"])
            self.collection_alerta.insert_one(informacion)
        elif informacion["tipo_mensaje"] == "Temperatura":
            informacion["TS"] = datetime.fromtimestamp(informacion["TS"])
            self.collection_temperatura.insert_one(informacion)
        elif informacion["tipo_mensaje"] == "Humedad":
            info2 = informacion
            informacion["TS"] = datetime.fromtimestamp(informacion["TS"])
            self.collection_temperatura.insert_one(informacion)
            self.sumarHumedades(info2)
        else:
            informacion["TS"] = datetime.fromtimestamp(informacion["TS"])
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
                "TS_FOG":timestamp,
            }
            print(f"humedad general {result}")
            result["TS"] = datetime.fromtimestamp(result["TS"])
            self.collection_temperatura.insert_one(result)
            self.sumatoriahumedad =0
            if valor > environment.MAX_HUMEDAD:
                alerta = {
                    "tipo_mensaje": "Alerta",
                    "valor": valor,
                    "TS": timestamp,
                    "TS_FOG":timestamp,
                }
                alerta["TS"] = datetime.fromtimestamp(alerta["TS"])
                self.collection_alerta.insert_one(alerta)
                self.senderSC.connect(
                    f"tcp://{environment.SC_CLOUD['host']}:{environment.SC_CLOUD['port']}"
                )
                msg = f"Alarma promedio humedad: {valor} por encima del valor maximo"
                self.senderSC.send_string(msg)
                msg_in = self.senderSC.recv_string()
                print(msg_in)

    def sumarHumedades(self, result):
        self.sumatoriahumedad += result["valor"]


def signal_handler(sig, frame):
    print("Interrupt received, stopping Scalene profiler...")
    exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    cloud = Cloud()
    cloud.inicializar()


if __name__ == "__main__":
    main()
