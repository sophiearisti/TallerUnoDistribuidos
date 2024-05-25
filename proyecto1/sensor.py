from abc import ABC, abstractmethod
import zmq

class Sensor:
    id_Contador = 0

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores):
        self.tipo = tipo
        self.prob_correctos = prob_correctos
        self.prob_fuera_rango = prob_fuera_rango
        self.prob_errores = prob_errores
        Sensor.id_Contador += 1
        self.pid = Sensor.id_Contador

    def generarAlerta(self, muestra):
        print("Generar alerta al sistema de calidad")

    @abstractmethod
    def obtenerMuestra(self):
        pass

    @abstractmethod
    def generarValores(self):
        pass

    @abstractmethod
    def enRango(self, muestra):
        pass
