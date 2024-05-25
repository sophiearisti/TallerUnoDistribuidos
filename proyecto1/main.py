import threading
from SensorHumo import SensorHumo
from SensorHumedad  import SensorHumedad
from SensorTemperatura  import SensorTemperatura
from constants import environment

def start( ):
    print(f"INICIALIZANDO LOS SENSORES")
    for _ in range(environment.CANT_SENSORES):
        thread = threading.Thread(target = create_sensor, args = (environment.SENSOR_TEMPERATURA,environment.ARCHIVO_TEMPERATURA))
        thread.start()

    for _ in range(environment.CANT_SENSORES):
        thread = threading.Thread(target = create_sensor, args = (environment.SENSOR_HUMEDAD,environment.ARCHIVO_HUMEDAD))
        thread.start()

    for _ in range(environment.CANT_SENSORES):
        thread = threading.Thread(target = create_sensor, args = (environment.SENSOR_HUMO,environment.ARCHIVO_HUMO))
        thread.start()


def create_sensor(nombre, archivo):
    prob_correctos, prob_fuera_rango, prob_errores=leerArchivo(archivo)
    if(nombre==environment.SENSOR_HUMO):
        sensor=SensorHumo(nombre,prob_correctos, prob_fuera_rango, prob_errores)
        sensor.generarValores()
    elif(nombre==environment.SENSOR_HUMEDAD):
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
    return float(variable1), float(variable2), float(variable3)

#MAIN
print("[ENCENDIENDO]")
start( )

