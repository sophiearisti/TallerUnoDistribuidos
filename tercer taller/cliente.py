import json
import time
import paho.mqtt.client as mqtt
import socket

mqttBroker = "mqtt.eclipseprojects.io"
FORMAT = "utf-8"
ipCliente = socket.gethostbyname(socket.gethostname())
respuesta = False

# Definición de la función de devolución de llamada on_message
def on_message(client, userdata, message):
    global respuesta
    print(f"Recibido: {message.payload.decode(FORMAT)}")
    respuesta = True
    client.disconnect() #Desconectar el cliente MQTT
    client.loop_stop()

#Obtener los valores de los catetos
print("Ingresa los el valor de los catetos para calcular la hipotenusa")
numero1 = input("Ingresa el valor del primer cateto:")
numero2 = input("Ingresa el valor del segundo cateto:")

# Crear un cliente MQTT
client = mqtt.Client(2, "CLIENTE")
client.connect(mqttBroker)

#Convertir y mandar valores
enviar = json.dumps({"numero1": float(numero1), "numero2": float(numero2), "ip": ipCliente})
client.publish("PETICION", enviar)
print(f"Enviado: {enviar} al tema PETICION")

# Bucle de espera de la respuesta
client.loop_start()
client.subscribe(ipCliente) #Suscribirse al tema RESPUESTA
client.on_message = on_message # Asociación de la función de devolución de llamada on_message al cliente MQTT
time.sleep(10) #Esperar a que llegue la respuesta

#Desconectar el cliente MQTT SI NO LLEGA LA RESPUESTA
if not respuesta:
    print("No se recibió respuesta")
    client.disconnect()
    client.loop_stop()