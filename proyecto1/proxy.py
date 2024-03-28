import zmq
from constants import environment

class Proxy:

    rangos = {"humedad": (70, 100), "temperatura": (11, 29.4), "humo": (True, False)}

    ip_cloud = ""
    ip_SC = ""
    ip_propia = "192.168.193.79"

    def inicializar(self):

        context = zmq.Context()
        # Socket to receive messages on
        receiver = context.socket(zmq.PULL)
        receiver.bind(f"tcp://{self.ip_propia}:5558")

        print("INICIALIZANDO PROXY")

        while True:
            print("RECIBIENDO MENSAJES...")
            result = receiver.recv_json()
            print(f"resultado recibido: {result}")

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
    # Crear una instancia del proxy
    proxy = Proxy()
    # Inicializar el proxy
    proxy.inicializar()


if __name__ == "__main__":
    main()
