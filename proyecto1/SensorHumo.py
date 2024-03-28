import time
import random
from Sensor import Sensor



class SensorHumo(Sensor):

    max=True
    min=False
    tiempo=5

    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores):
        super().__init__(tipo, prob_correctos, prob_fuera_rango, prob_errores)

    def obtenerMuestra(self):
        return random.uniform(11, 29.4)

    def generarValores(self):

        self.sender_proxy.connect(f"tcp://{self.ip_proxy}:5558")

        print("ENCENDIENDO...")

        while True:
            
            muestra = self.obtenerMuestra()

            tipo_mensaje = self.enRango(muestra)

            if(tipo_mensaje=="Alerta"):
                self.generarAlerta(muestra)

            result = { 'tipo_sensor' : self.tipo,'tipo_mensaje' : tipo_mensaje, 'valor' : muestra}

            print(f"ENVIADO MENSAJE {self.tipo}: tipo_mensaje {tipo_mensaje} valor {muestra}")
            
            self.sender_proxy.send_json(result)

            time.sleep(self.tiempo)

    def enRango(self,muestra):
        if(muestra==self.min):
            return "Muestra"
        else:
            return"Alerta"
        
    def generarAlerta(self,muestra):
        print("generar alerta al sistema de calidad")
        print("generar alerta al aspersor")
