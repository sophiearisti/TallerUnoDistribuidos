import json
import random
import time
from datetime import datetime

import zmq
from constants import environment
from sensor import Sensor
from datetime import datetime

class SensorErroneo(Sensor):
    max = environment.MAX_HUMEDAD
    min = environment.MIN_HUMEDAD
    tiempo = environment.TIEMPO_HUMEDAD

    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores,contador):
        super().__init__(tipo, prob_correctos, prob_fuera_rango, prob_errores,contador) # type: ignore

    def generarValores(self):
        print(f"ENCENDIENDO SENSOR HUMEDAD CON ID {self.pid}...")
        self.socket.connect(
            f'tcp://{environment.BROKER_SOCKET["host"]}:{environment.BROKER_SOCKET["sub_port"]}'
        )
        time.sleep(1)

        while True:

            timestamp = time.time()
            result = {
                "tipo_sensor": "MALO",
                "tipo_mensaje": "PING",
                "valor": -15,
                "TS": timestamp,
                "id": self.pid,
            }

            print(
                f"ENVIADO MENSAJE MALO CON ID {self.pid}: tipo_mensaje PING valor -15 tiempo {datetime.fromtimestamp(timestamp)}"
            )

            message = json.dumps(result)
            self.socket.send(bytes(f"SENSOR {message}", 'utf-8'))
            time.sleep(3)


