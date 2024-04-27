import json
import socket
import time

import paho.mqtt.client as mqtt

# Obtener la dirección IP de la máquina local
LOCALHOST = socket.gethostbyname(socket.gethostname())

# Variable global para indicar si se ha recibido un mensaje
mensaje_recibido = False

# Definición de la función de devolución de llamada on_message
def on_message(client, userdata, message):
    global mensaje_recibido  # Declarar la variable global
    print("Mensaje recibido en el tema:", message.topic)
    
    # Decodificar el JSON recibido
    json_data = json.loads(message.payload.decode("utf-8"))
    
    # Obtener la respuesta del JSON
    respuesta = json_data["respuesta"]
    print("Respuesta recibida:", respuesta)
    
    # Detener el bucle de eventos y desconectar el cliente MQTT
    client.loop_stop()
    client.disconnect()
    
    # Actualizar la variable global
    mensaje_recibido = True


print("Ingresa los el valor de los catetos para calcular la hipotenusa")
numero1 = input("Ingresa el valor del primer cateto:")
numero2 = input("Ingresa el valor del segundo cateto:")

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "CLIENTE")

client.connect(mqttBroker)

enviar = json.dumps({"numero1": float(numero1), "numero2": float(numero2), "topic": LOCALHOST})

client.publish("PETICION", enviar)

# Convertir la cadena JSON de vuelta a un diccionario
enviar_dict = json.loads(enviar)

print(
    "publicado: val1 "
    + str(enviar_dict["numero1"])
    + " val2 "
    + str(enviar_dict["numero2"])
    + " topic "
    + enviar_dict["topic"]
    + " al tema PETICION"
)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"RESPUESTA")

# Conexión al broker MQTT y suscripción al tema "test/topic"
client.connect(mqttBroker)
client.subscribe(LOCALHOST)

# Asociación de la función de devolución de llamada on_message al cliente MQTT
client.on_message = on_message

# Inicio del bucle de eventos del cliente MQTT
client.loop_start()

# Bucle principal para mantener el script en ejecución
while not mensaje_recibido:
    time.sleep(1)

# Si se interrumpe manualmente el script, detener el bucle de eventos y desconectar el cliente MQTT
client.disconnect()
client.loop_stop()
