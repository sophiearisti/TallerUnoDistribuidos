import time
import random
from Sensor import Sensor
from constants import environment
from datetime import datetime


class SensorTemperatura(Sensor):

    max = 29.4
    min = 11
    tiempo = 6

    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores):
        super().__init__(tipo, prob_correctos, prob_fuera_rango, prob_errores)

    def obtenerMuestra(self):
        probability = random.random()

        if probability < self.prob_correctos:
            return "{:.1f}".format(random.uniform(self.min, self.max))

        elif probability < self.prob_correctos + self.prob_fuera_rango:
            if probability < 0.5:
                return "{:.1f}".format(random.uniform(0.1, self.min) - 0.1)
            else:
                return "{:.1f}".format(random.uniform(self.max, 99.9) + 0.1)

        else:
            return "{:.1f}".format(random.uniform(-self.min, -0.1))

    def generarValores(self):

        self.sender_proxy.connect(f"tcp://{self.ip_proxy}:5558")

        print(f"ENCENDIENDO SENSOR TEMPERATURA CON ID {self.pid}...")

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
                "id":self.pid 
            }

            print(
                f"ENVIADO MENSAJE {self.tipo} CON ID {self.pid}: tipo_mensaje {tipo_mensaje} valor {muestra} tiempo {datetime.fromtimestamp(timestamp)}"
            )

            self.sender_proxy.send_json(result)

            time.sleep(self.tiempo)

    def enRango(self, muestra):
        if muestra > self.min and muestra < self.max:
            return environment.TIPO_RESULTADO_MUESTRA
        elif muestra < 0:
            return environment.TIPO_RESULTADO_ERROR
        else:
            return environment.TIPO_RESULTADO_ALERTA
