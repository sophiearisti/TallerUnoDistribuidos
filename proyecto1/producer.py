import time
import zmq
import random

probabilidadErroneo = 0.5
probabilidadCorrecto = 0.4
probabilidadFuera = 0.1

def obtenerMuestra():
    return random.uniform(11, 29.4)

def enviarValor():
    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    ip = "192.168.193.79"

    sender.connect(f"tcp://{ip}.79:5558")

    print("ENCENDIENDO...")

    while True:
        tipo_mensaje = "dato"
        tipo_sensor = "temperatura"
        muestra = obtenerMuestra()
        result = { 'tipo_sensor' : tipo_sensor,'tipo_mensaje' : tipo_mensaje, 'valor' : muestra}

        print(f"ENVIADO MENSAJE: tipo_mensaje {tipo_mensaje} valor {muestra}")
        
        sender.send_json(result)

        time.sleep(6)

enviarValor()