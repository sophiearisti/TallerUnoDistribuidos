import queue
import threading
import zmq
import json
from datetime import datetime
from constants import environment
import time
import asyncio


class Fog:
    rangos = {"humedad": (70, 100), "temperatura": (11, 29.4), "humo": (True, False)}
    context = zmq.Context()
    senderSC = context.socket(zmq.REQ)
    senderCloud = context.socket(zmq.REQ)

    colors = {
        "Error": "\033[93m",  # Yellow
        "Muestra": "\033[92m",  # Green
        "Alerta": "\033[91m",  # Red
    }
    reset_color = "\033[0m"

    def get_color(self, tipo_mensaje):
        return self.colors.get(tipo_mensaje, "")

    def inicializar(self):
        receiver = self.context.socket(zmq.SUB)
        receiver.connect(
            f'tcp://{environment.BROKER_SOCKET["host"]}:{environment.BROKER_SOCKET["pub_port"]}'
        )
        receiver.setsockopt(zmq.SUBSCRIBE, bytes("SENSOR", "utf-8"))

        print("INICIALIZANDO PROXY")
        # Iniciar el bucle de enviarPromedioHumedad en un hilo separado
        threading.Thread(target=self.enviarPromedioHumedad).start()

        while True:
            print("RECIBIENDO MENSAJES...")
            message = receiver.recv_multipart()
            # Obtener la cadena de bytes del primer elemento de la lista
            message_bytes = message[0]

            # Decodificar los bytes a una cadena de texto
            message_text = message_bytes.decode("utf-8")

            # Dividir la cadena de texto en dos partes en el primer espacio
            topic, json_result = message_text.split(" ", 1)
            result = json.loads(json_result)

            color = self.get_color(result["tipo_mensaje"])
            print(
                f"HORA:\t {datetime.fromtimestamp(result['TS'])}\tSENSOR:\t{result['tipo_sensor']}\tID:\t{result['id']}\tVALOR:\t{result['valor']}\tTIPO MENSAJE\t{color}{result['tipo_mensaje']}{self.reset_color}"
            )

            if self.validar(result):
                print("VALORES CORRECTOS")
                if result["tipo_sensor"] == "temperatura":
                    self.calcularTemperatura(result)
                elif result["tipo_sensor"] == "humedad":
                    self.calcularHumedad(result)
            else:
                print("VALORES INCORRECTOS")

            self.enviar_cloud(result)

    def validar(self, result):
        tipo_sensor = result["tipo_sensor"]
        valor = result["valor"]
        tipo_mensaje = result["tipo_mensaje"]

        if tipo_sensor == "humo":
            return self.enRangoHumo(valor, tipo_mensaje)
        elif tipo_sensor in ["humedad", "temperatura"]:
            return self.enRango(valor, *self.rangos[tipo_sensor], tipo_mensaje) # type: ignore
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

    def enviar_cloud(self, mensaje):
        self.senderCloud.connect(
            f"tcp://{environment.CLOUD['host']}:{environment.CLOUD['port']}"
        )
        self.senderCloud.send_json(mensaje)
        msg_in = self.senderCloud.recv_string()
        print(msg_in)

    colas_temperaturas = [queue.Queue() for _ in range(environment.CANT_SENSORES)]

    def calcularTemperatura(self, result):
        sensor_id = result["id"] - 1
        self.colas_temperaturas[sensor_id].put(result)

        if all(not q.empty() for q in self.colas_temperaturas):
            print("Promedio de los 10 sensores de temperatura: ")
            total_sum = 0
            for i, q in enumerate(self.colas_temperaturas):
                front_result = q.get()  # Dequeue the front value
                total_sum += front_result["valor"]
                print(f"Valor del sensor del promedio: {front_result}")

            promedio = total_sum / environment.CANT_SENSORES
            print(f"Promedio temperatura: {promedio}")
            timestamp = time.time()
            result = {
                "tipo_mensaje": "Temperatura",
                "valor": promedio,
                "TS": timestamp,
            }
            self.enviar_cloud(result)

    sumatoriahumedad = 0

    def calcularHumedad(self, result):
       self.sumatoriahumedad += result["valor"]

    def enviarPromedioHumedad(self):
        context_promedio = zmq.Context()
        senderCloud_promedio = context_promedio.socket(zmq.REQ)
        while True:
            time.sleep(5)
            valor = self.sumatoriahumedad / environment.CANT_SENSORES
            timestamp = time.time()
            result = {
                "tipo_mensaje": "Humedad",
                "valor": valor,
                "TS": timestamp,
            }
            self.sumatoriahumedad = 0
            senderCloud_promedio.connect(
            f"tcp://{environment.CLOUD['host']}:{environment.CLOUD['port']}")
            senderCloud_promedio.send_json(result)
            msg_in = senderCloud_promedio.recv_string()
            print(msg_in)


def main():
    proxy = Fog()
    proxy.inicializar()

if __name__ == "__main__":
    main()
