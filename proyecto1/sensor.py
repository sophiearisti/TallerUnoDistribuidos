from abc import ABC, abstractmethod

import zmq


class Sensor:
    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores, contador):
        self.tipo = tipo
        self.prob_correctos = prob_correctos
        self.prob_fuera_rango = prob_fuera_rango
        self.prob_errores = prob_errores
        self.pid = contador
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.senderSC = self.context.socket(zmq.REQ)

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
