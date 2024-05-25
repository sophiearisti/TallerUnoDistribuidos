
import zmq
import json
from datetime import datetime
from constants import environment

class Fog:
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

    def inicializar(self):
        context = zmq.Context()
        receiver = context.socket(zmq.SUB)
        receiver.connect(f'tcp://localhost:{environment.BROKER_SOCKET["pub_port"]}')
        receiver.setsockopt(zmq.SUBSCRIBE, bytes("SENSOR", 'utf-8'))

        print("INICIALIZANDO PROXY")

        while True:
            print("RECIBIENDO MENSAJES...")
            message = receiver.recv_multipart()
            # Obtener la cadena de bytes del primer elemento de la lista
            message_bytes = message[0]

            # Decodificar los bytes a una cadena de texto
            message_text = message_bytes.decode('utf-8')

            # Dividir la cadena de texto en dos partes en el primer espacio
            topic, json_result = message_text.split(' ', 1)
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

def main():
    proxy = Fog()
    proxy.inicializar()

if __name__ == "__main__":
   main()