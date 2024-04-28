import paho.mqtt.client as mqtt
import time
import json

FORMAT = "utf-8"
mqttBroker = "broker.hivemq.com"

def on_message(client, userdata, message):
    print(f"Recibido: {message.payload.decode('utf-8')} del tema {message.topic}")
    json_message = json.loads(message.payload.decode('utf-8'))
    client.publish(json_message["tema"], pow(float(json_message["numero2"]),2))
    print(f"Enviado: {pow(float(json_message["numero2"]),2)} al tema RESPUESTA_CATETO2")

print("[ENCENDIENDO] SERVIDOR CALCULO2")
# Crear un cliente MQTT
client = mqtt.Client(2,"CALCULO2")
client.connect(mqttBroker)

try:
    while True:
        client.loop_start()
        client.subscribe("CATETO2")
        client.on_message = on_message
        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()