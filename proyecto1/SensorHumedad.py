import random
import time
from constants import environment
from Sensor import Sensor
from datetime import datetime


class SensorHumedad(Sensor):

    max = environment.MAX_HUMEDAD
    min = environment.MIN_HUMEDAD
    tiempo = environment.TIEMPO_HUMEDAD

    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores):
        super().__init__(tipo, prob_correctos, prob_fuera_rango, prob_errores)

    def obtenerMuestra(self):
        probability = random.random()

        if probability < self.prob_correctos:
            return "{:.1f}".format(random.uniform(self.min, self.max))

        elif probability < self.prob_correctos + self.prob_fuera_rango:
            return "{:.1f}".format(random.uniform(-0.1, self.min) - 0.1)

        else:
            return "{:.1f}".format(random.uniform(-self.min, 0) - 0.1)

    def generarValores(self):

        print(f"ENCENDIENDO SENSOR HUMEDAD CON ID {self.pid}...")

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
                "TS": time.time(),
                "id": self.pid
            }

            print(
                f"ENVIADO MENSAJE {self.tipo} CON ID {self.pid}: tipo_mensaje {tipo_mensaje} valor {muestra} tiempo {datetime.fromtimestamp(timestamp)}"
            )

            self.socket.send_json(result)

            time.sleep(self.tiempo)

    def enRango(self, muestra):
        if muestra > self.min and muestra < self.max:
            return environment.TIPO_RESULTADO_MUESTRA
        elif muestra < 0:
            return environment.TIPO_RESULTADO_ERROR
        else:
            return environment.TIPO_RESULTADO_ALERTA
