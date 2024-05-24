from abc import ABC, abstractmethod
import zmq.asyncio
from constants import environment

class Sensor:
    id_Contador = 0

    context = zmq.asyncio.Context()
    socket = context.socket(zmq.PUB)
    socket.connect(f'tcp://{environment.BROKER_SOCKET["host"]}:{environment.BROKER_SOCKET["pub_port"]}')

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
    async def generarValores(self):
        pass

    @abstractmethod
    def enRango(self, muestra):
        pass
