import paho.mqtt.client as mqtt
import time
import json
import socket

FORMAT = "utf-8"
mqttBroker = "broker.hivemq.com"
ipServidor = socket.gethostbyname(socket.gethostname())

def on_message(client, userdata, message):
    print(f"Recibido: {message.payload.decode('utf-8')} del tema {message.topic}")
    json_message = json.loads(message.payload.decode('utf-8'))
    client.publish(json_message["tema"], pow(float(json_message["numero1"]),2))
    print(f"Enviado: {pow(float(json_message["numero1"]),2)} al tema RESPUESTA_CATETO1")

print("[ENCENDIENDO] SERVIDOR CALCULO1")
# Crear un cliente MQTT
client = mqtt.Client(2,ipServidor+"S1")
client.connect(mqttBroker)

try:
    while True:
        client.loop_start()
        client.subscribe("CATETO1")
        client.on_message = on_message
        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()