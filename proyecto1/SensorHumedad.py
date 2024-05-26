import json
import random
import time
from datetime import datetime

import zmq

from constants import environment
from sensor import Sensor


class SensorHumedad(Sensor):
    max = environment.MAX_HUMEDAD
    min = environment.MIN_HUMEDAD
    tiempo = environment.TIEMPO_HUMEDAD

    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores, contador):
        super().__init__(tipo, prob_correctos, prob_fuera_rango, prob_errores, contador)  # type: ignore

    def obtenerMuestra(self):
        probability = random.random()

        if probability < self.prob_correctos:
            return "{:.1f}".format(random.uniform(self.min, self.max))
        elif probability < self.prob_correctos + self.prob_fuera_rango:
            return "{:.1f}".format(random.uniform(self.max + 0.1, self.max + 10))
        else:
            return "{:.1f}".format(random.uniform(-self.min, -0.1))

    def generarValores(self):
        print(f"ENCENDIENDO SENSOR HUMEDAD CON ID {self.pid}...")
        self.socket.connect(
            f'tcp://{environment.BROKER_SOCKET["host"]}:{environment.BROKER_SOCKET["sub_port"]}'
        )
        time.sleep(1)

        while True:
            muestra = float(self.obtenerMuestra())
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
        if self.min <= muestra <= self.max:
            return environment.TIPO_RESULTADO_MUESTRA
        elif muestra < 0:
            return environment.TIPO_RESULTADO_ERROR
        else:
            return environment.TIPO_RESULTADO_ALERTA

    def generarAlerta(self, muestra):
        self.senderSC.connect(
            f"tcp://{environment.SC_EDGE['host']}:{environment.SC_EDGE['port']}"
        )
        msg = f"Alarma humedad: {muestra}. Sensor con id {self.pid}"
        self.senderSC.send_string(msg)
        msg_in = self.senderSC.recv_string()
        print(msg_in)
