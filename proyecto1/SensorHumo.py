import time
import random
from Sensor import Sensor
from constants import environment

class SensorHumo(Sensor):

    max=environment.MAX_HUMO
    min=environment.MIN_HUMO
    tiempo=environment.TIEMPO_HUMO

    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores):
        super().__init__(tipo, prob_correctos, prob_fuera_rango, prob_errores)

    def obtenerMuestra(self):
        probability = random.random()

        if probability < self.prob_errores:
            return None

        else:
            probability = random.random()
            if probability < 0.5:
                return self.max
            else:
                return self.min
        
    def generarValores(self):

        self.sender_proxy.connect(f"tcp://{self.ip_proxy}:5558")

        print(f"ENCENDIENDO SENSOR HUMO CON ID {self.pid}...")

        while True:
            
            muestra = self.obtenerMuestra()

            tipo_mensaje = self.enRango(muestra)

            if(tipo_mensaje==environment.TIPO_RESULTADO_ALERTA):
                self.generarAlerta(muestra)

            result = { 'tipo_sensor' : self.tipo,'tipo_mensaje' : tipo_mensaje, 'valor' : muestra}

            print(f"ENVIADO MENSAJE {self.tipo} CON ID {self.pid}: tipo_mensaje {tipo_mensaje} valor {muestra}")
            
            self.sender_proxy.send_json(result)

            time.sleep(self.tiempo)

    def enRango(self,muestra):
        if(muestra==self.min):
            return environment.TIPO_RESULTADO_MUESTRA
        elif(muestra==self.max):
            return environment.TIPO_RESULTADO_ALERTA
        else:
            return environment.TIPO_RESULTADO_ERROR
        
    def generarAlerta(self,muestra):
        print("generar alerta al sistema de calidad")
        print("generar alerta al aspersor")
