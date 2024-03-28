import zmq


class Proxy:

    rangos = {"humedad": (70, 100), "temperatura": (11, 29.4), "humo": (True, False)}

    ip_cloud = ""
    ip_SC = ""
    ip_propia = "192.168.193.126"
    #ip_propia = "192.168.193.79"
    #sender_SC = context.socket(zmq.REQ)
    #sender_Cloud = context.socket(zmq.REQ)

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
            
            if(self.validar(result)):
                print("VALORES CORRECTOS")
            else:
                print("VALORES INCORRECTOS")
            

    def validar(self, result):
        if(result['tipo_sensor']=="humo"):

            if(result['tipo_mensaje']=="Muestra" and self.enRangoHumo(result['muestra'])):
                return True

        elif(result['tipo_sensor']=="humedad"):
            if(result['tipo_mensaje']=="Muestra" and self.enRango(result['muestra'], self.rangos['humedad'][0], self.rangos['humedad'][1])):
                return True

        else: #es temperatura
            if(result['tipo_mensaje']=="Muestra" and self.enRango(result['muestra'], self.rangos['temperatura'][0], self.rangos['temperatura'][1])):
                return True
        
        return False

    def enRango(self,muestra, min, max):
        if(muestra>min and muestra<max):
            return True
        else:
            return False
    
    def enRangoHumo(self,muestra):
        if(muestra==False):
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