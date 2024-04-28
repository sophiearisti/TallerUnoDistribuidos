import paho.mqtt.client as mqtt
import time

FORMAT = "utf-8"
mqttBroker = "mqtt.eclipseprojects.io"

def on_message(client, userdata, message):
    print(f"Recibido: {message.payload.decode('utf-8')} del tema {message.topic}")
    client.publish("RESPUESTA_CATETO1", pow(float(message.payload.decode('utf-8')),2))
    print(f"Enviado: {pow(float(message.payload.decode('utf-8')),2)} al tema RESPUESTA_CATETO1")

print("[ENCENDIENDO] SERVIDOR CALCULO1")
# Crear un cliente MQTT
client = mqtt.Client(2,"CALCULO1")
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