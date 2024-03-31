from abc import abstractmethod
from constants import environment
import zmq
import os
import random

class Sensor:

    
    ip_proxy = environment.IP_PROXY
    ip_SC=environment.IP_SC_EDGE
    context = zmq.Context()
    sender_proxy = context.socket(zmq.PUSH)
    sender_SC = context.socket(zmq.REQ)

    def __init__(self, tipo, prob_correctos, prob_fuera_rango, prob_errores):
        self.tipo = tipo
        self.prob_correctos = prob_correctos
        self.prob_fuera_rango = prob_fuera_rango
        self.prob_errores = prob_errores
        self.pid ="{:.1f}".format(os.getpid()+random.uniform(0,10000))

    def generarAlerta(self,muestra):
        print("generar alerta al sistema de calidad")

    @abstractmethod
    def obtenerMuestra(self):
        pass

    @abstractmethod
    def generarValores(self):
        pass

    @abstractmethod
    def enRango(self,muestra):
        pass


 