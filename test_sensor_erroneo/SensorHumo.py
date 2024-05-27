import asyncio
import json
import random
import time
from datetime import datetime

import zmq

from constants import environment
from sensor import Sensor


class SensorHumo(Sensor):

    max = environment.MAX_HUMO
    min = environment.MIN_HUMO
    tiempo = environment.TIEMPO_HUMO

    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores, contador):
        super().__init__(tipo, prob_correctos, prob_fuera_rango, prob_errores, contador) # type: ignore
        self.context_aspersor = zmq.Context()
        self.sender_aspersor = self.context_aspersor.socket(zmq.REQ)

    def obtenerMuestra(self):
        probability = random.random()

        if probability < self.prob_errores:
            return None

        probability = random.random()
        if probability < 0.5:
            return self.max
        else:
            return self.min

    def generarValores(self):
        print(f"ENCENDIENDO SENSOR HUMO CON ID {self.pid}...")
        self.socket.connect(
            f'tcp://{environment.BROKER_SOCKET["host"]}:{environment.BROKER_SOCKET["sub_port"]}'
        )
        time.sleep(1)

        while True:
            muestra = self.obtenerMuestra()
            tipo_mensaje = self.enRango(muestra)

            if tipo_mensaje == environment.TIPO_RESULTADO_ALERTA:
                self.generarAlerta(muestra)

            timestamp = time.time()
            result = {
                "tipo_sensor": self.tipo,
                "tipo_mensaje": tipo_mensaje,
                "valor": muestra,
                "TS": timestamp,
                "id": self.pid,
            }

            print(
                f"ENVIADO MENSAJE {self.tipo} CON ID {self.pid}: tipo_mensaje {tipo_mensaje} valor {muestra} tiempo {datetime.fromtimestamp(timestamp)}"
            )

            message = json.dumps(result)
            self.socket.send(bytes(f"SENSOR {message}", "utf-8"))
            time.sleep(self.tiempo)

    def enRango(self, muestra):
        if muestra == self.min:
            return environment.TIPO_RESULTADO_MUESTRA
        elif muestra == self.max:
            return environment.TIPO_RESULTADO_ALERTA
        else:
            return environment.TIPO_RESULTADO_ERROR

    def generarAlerta(self, muestra):
        self.sistemaCalidad(muestra)
        self.aspersor()

    def aspersor(self):
        self.sender_aspersor.connect(
            f"tcp://{environment.ASPERSOR['host']}:{environment.ASPERSOR['port']}"
        )
        msg = f"Activar aspersor. Sensor con id {self.pid}"
        self.sender_aspersor.send_string(msg)
        msg_in = self.sender_aspersor.recv_string()
        print(msg_in)

    def sistemaCalidad(self, muestra):
        self.senderSC.connect(
            f"tcp://{environment.SC_EDGE['host']}:{environment.SC_EDGE['port']}"
        )
        msg = f"Alarma humo: {muestra}. Sensor con id {self.pid}"
        self.senderSC.send_string(msg)
        msg_in = self.senderSC.recv_string()
        print(msg_in)
