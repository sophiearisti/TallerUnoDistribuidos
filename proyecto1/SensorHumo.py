import time
import random
import json
from sensor import Sensor
from constants import environment
from datetime import datetime
import asyncio

class SensorHumo(Sensor):
    max = environment.MAX_HUMO
    min = environment.MIN_HUMO
    tiempo = environment.TIEMPO_HUMO

    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores):
        super().__init__(tipo, prob_correctos, prob_fuera_rango, prob_errores)

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
            self.socket.send(bytes(f"SENSOR {message}", 'utf-8'))
            time.sleep(self.tiempo)

    def enRango(self, muestra):
        if muestra == self.min:
            return environment.TIPO_RESULTADO_MUESTRA
        elif muestra == self.max:
            return environment.TIPO_RESULTADO_ALERTA
        else:
            return environment.TIPO_RESULTADO_ERROR

    def generarAlerta(self, muestra):
        print("Generar alerta al sistema de calidad")
        print("Generar alerta al aspersor")

