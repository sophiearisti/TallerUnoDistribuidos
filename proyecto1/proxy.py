import asyncio
import zmq
import zmq.asyncio
import json
from datetime import datetime
from constants import environment

class Proxy:
    rangos = {"humedad": (70, 100), "temperatura": (11, 29.4), "humo": (True, False)}
    ip_cloud = ""
    ip_SC = ""
    ip_propia = "192.168.193.79"

    colors = {
        'Error': '\033[93m',    # Yellow
        'Muestra': '\033[92m',  # Green
        'Alerta': '\033[91m',   # Red
    }
    reset_color = '\033[0m'

    def get_color(self, tipo_mensaje):
        return self.colors.get(tipo_mensaje, '')

    async def inicializar(self):
        context = zmq.asyncio.Context()
        receiver = context.socket(zmq.SUB)
        receiver.connect(f'tcp://{environment.BROKER_SOCKET["host"]}:{environment.BROKER_SOCKET["sub_port"]}')
        receiver.setsockopt_string(zmq.SUBSCRIBE, "SENSOR")

        print("INICIALIZANDO PROXY")

        while True:
            print("RECIBIENDO MENSAJES...")
            message = await receiver.recv_string()
            topic, json_result = message.split(' ', 1)
            result = json.loads(json_result)

            color = self.get_color(result['tipo_mensaje'])
            print(f"HORA:\t {datetime.fromtimestamp(result['TS'])}\tSENSOR:\t{result['tipo_sensor']}\tID:\t{result['id']}\tVALOR:\t{result['valor']}\tTIPO MENSAJE\t{color}{result['tipo_mensaje']}{self.reset_color}")

            if self.validar(result):
                print("VALORES CORRECTOS")
            else:
                print("VALORES INCORRECTOS")

    def validar(self, result):
        tipo_sensor = result["tipo_sensor"]
        valor = result["valor"]
        tipo_mensaje = result["tipo_mensaje"]

        if tipo_sensor == "humo":
            return self.enRangoHumo(valor, tipo_mensaje)
        elif tipo_sensor in ["humedad", "temperatura"]:
            return self.enRango(valor, *self.rangos[tipo_sensor], tipo_mensaje)
        else:
            return False

    def enRango(self, muestra, min, max, tipo_mensaje):
        if min <= muestra <= max and tipo_mensaje == "Muestra":
            return True
        elif muestra < 0 and tipo_mensaje == "Error":
            return True
        elif muestra not in [False, True] and tipo_mensaje == "Alerta":
            return True
        else:
            return False

    def enRangoHumo(self, muestra, tipo_mensaje):
        if muestra is False and tipo_mensaje == "Muestra":
            return True
        elif muestra is True and tipo_mensaje == "Alerta":
            return True
        elif muestra is None and tipo_mensaje == "Error":
            return True
        else:
            return False

async def main():
    proxy = Proxy()
    await proxy.inicializar()

if __name__ == "__main__":
    asyncio.run(main())