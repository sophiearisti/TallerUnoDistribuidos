from math import sqrt
import paho.mqtt.client as mqtt
import time
import json

FORMAT = "utf-8"
mqttBroker = "broker.hivemq.com"

def on_message(client, userdata, message):
    print(f"Recibido: {message.payload.decode('utf-8')} del tema {message.topic}")
    json_data = json.loads(message.payload.decode(FORMAT))
    hipotenusa = sqrt(float(json_data["cateto1"])+float(json_data["cateto2"]))
    client.publish(json_data["tema"], hipotenusa)
    print(f"Enviado: {hipotenusa} al tema RESPUESTA_HIPOTENUSA")

print("[ENCENDIENDO] SERVIDOR CALCULO3")
# Crear un cliente MQTT
client = mqtt.Client(2,"HIPOTENUSA")
client.connect(mqttBroker)

try:
    while True:
        client.loop_start()
        client.subscribe("HIPOTENUSA")
        client.on_message = on_message
        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()