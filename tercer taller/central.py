import time
import paho.mqtt.client as mqtt
import json
import socket
from math import sqrt

FORMAT = "utf-8"
mqttBroker = "broker.hivemq.com"
ipCliente = ""
json_data = {}
received_cateto1 = False; received_cateto2 = False; hipotenusa_mandado = False; peticion_recibida = False
cateto1 = 0.0; cateto2 = 0.0; timeout = 5; start_time = 0
ipCentral = socket.gethostbyname(socket.gethostname())

# Definición de qué hacer si llega una petición
def on_message_peticion(client, userdata, message):
    global ipCliente, json_data, received_cateto1, received_cateto2, hipotenusa_mandado, peticion_recibida, start_time
    print(f"Mensaje recibido: {message.payload.decode(FORMAT)} del tema {message.topic}")
    # Decodificar el mensaje JSON
    json_data = json.loads(message.payload.decode(FORMAT))
    # Resetear estado para una nueva petición
    received_cateto1 = False
    received_cateto2 = False
    hipotenusa_mandado = False
    peticion_recibida = True
    start_time = time.time()
    
    # Mandar el mensaje a los temas correspondientes1
    client.publish("CATETO1", json.dumps({"numero1": json_data["numero1"], "tema": ipCentral + "C1"}))
    client.publish("CATETO2", json.dumps({"numero2": json_data["numero2"], "tema": ipCentral + "C2"}))
    ipCliente = json_data["ip"]
    print(f"Enviado: {json_data['numero1']} al tema CATETO1")
    print(f"Enviado: {json_data['numero2']} al tema CATETO2")

# Definición de qué hacer si llega el cateto 1
def on_message_cateto1(client, userdata, message):
    global received_cateto1, cateto1
    print(f"Recibido: {message.payload.decode(FORMAT)} del tema {message.topic}")
    cateto1 = float(message.payload.decode(FORMAT))
    received_cateto1 = True

# Definición de qué hacer si llega el cateto 2
def on_message_cateto2(client, userdata, message):
    global received_cateto2, cateto2
    print(f"Recibido: {message.payload.decode(FORMAT)} del tema {message.topic}")
    cateto2 = float(message.payload.decode(FORMAT))
    received_cateto2 = True

# Definición de qué hacer si llega la hipotenusa
def on_message_hipotenusa(client, userdata, message):
    global ipCliente, cateto1, cateto2, hipotenusa_mandado, peticion_recibida
    hipotenusa_mandado = True
    print(f"Mensaje recibido: {message.payload.decode(FORMAT)} del tema {message.topic}")
    client.publish(ipCliente, float(message.payload.decode(FORMAT)))
    print(f"Enviado: {message.payload.decode(FORMAT)} al tema ipCliente")
    peticion_recibida = False

# Inicio del programa principal
print("[ENCENDIENDO] SERVIDOR CENTRAL")

# Crear un cliente MQTT
client = mqtt.Client(2, ipCentral)
client.connect(mqttBroker)
client.message_callback_add(ipCentral + "C1", on_message_cateto1)
client.subscribe(ipCentral + "C1")

# Definición de los callbacks
client.message_callback_add("PETICION", on_message_peticion)
client.message_callback_add(ipCentral + "C1", on_message_cateto1)
client.message_callback_add(ipCentral + "C2", on_message_cateto2)
client.message_callback_add(ipCentral + "H", on_message_hipotenusa)

# Bucle de eventos del cliente MQTT
client.loop_start()

# Suscribirse a los temas relevantes
client.subscribe("PETICION")
client.subscribe(ipCentral + "C1")
client.subscribe(ipCentral + "C2")
client.subscribe(ipCentral + "H")

# Mantener el script en ejecución
try:
    timeout = 5  # Tiempo de espera en segundos
    start_time = time.time()

    while True:
        time.sleep(1)
        if received_cateto1 and received_cateto2:
            client.publish("HIPOTENUSA", json.dumps({"cateto1": cateto1, "cateto2": cateto2, "tema": ipCentral + "H"}))
            print(f"Enviado: {cateto1} y {cateto2} al tema HIPOTENUSA")
            received_cateto1 = False; received_cateto2 = False
        # Verificar si ha ocurrido un timeout y no se ha enviado la hipotenusa
        if time.time() - start_time > timeout and not hipotenusa_mandado and peticion_recibida:
            # Calcular y publicar la hipotenusa con valores predeterminados
            hipotenusa = sqrt(float(json_data["numero1"]) ** 2 + float(json_data["numero2"]) ** 2)
            client.publish(ipCliente, hipotenusa)
            print(f"Enviado: {hipotenusa} al tema ipCliente")
            peticion_recibida = False

except KeyboardInterrupt:
    # Si se interrumpe manualmente el script, detener el bucle de eventos y desconectar el cliente MQTT
    client.disconnect()
    client.loop_stop()
