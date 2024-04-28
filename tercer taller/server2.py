import paho.mqtt.client as mqtt
import time

FORMAT = "utf-8"
mqttBroker = "mqtt.eclipseprojects.io"

def on_message(client, userdata, message):
    print(f"Recibido: {message.payload.decode('utf-8')} del tema {message.topic}")
    client.publish("RESPUESTA_CATETO2", pow(float(message.payload.decode('utf-8')),2))
    print(f"Enviado: {pow(float(message.payload.decode('utf-8')),2)} al tema RESPUESTA_CATETO2")

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