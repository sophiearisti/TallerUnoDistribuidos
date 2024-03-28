import threading
from SensorHumo import SensorHumo
from SensorHumedad  import SensorHumedad
from SensorTemperatura  import SensorTemperatura
from Sensor import Sensor

def start( ):
    print(f"INICIALIZANDO LOS SENSORES")
    for _ in range(10):
        thread = threading.Thread(target = create_sensor, args = ("temperatura","files/temperatura.txt"))
        thread.start()

    for _ in range(10):
        thread = threading.Thread(target = create_sensor, args = ("humedad","files/humedad.txt"))
        thread.start()

    for _ in range(10):
        thread = threading.Thread(target = create_sensor, args = ("humo","files/humo.txt"))
        thread.start()


def create_sensor(nombre, archivo):
    prob_correctos, prob_fuera_rango, prob_errores=leerArchivo(archivo)
    if(nombre=="humo"):
        sensor=SensorHumo(nombre,prob_correctos, prob_fuera_rango, prob_errores)
        sensor.generarValores()
    elif(nombre=="humedad"):
        sensor=SensorHumedad(nombre,prob_correctos, prob_fuera_rango, prob_errores)
        sensor.generarValores()
    else:
        sensor=SensorTemperatura(nombre,prob_correctos, prob_fuera_rango, prob_errores)
        sensor.generarValores()

    
def leerArchivo(nombre_archivo):
    print("Leyendo valores")
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.readline()
        partes = contenido.split(',')
        variable1, variable2, variable3 = partes[0], partes[1], partes[2]
    return variable1, variable2, variable3 

#MAIN
print("[ENCENDIENDO]")
start( )

