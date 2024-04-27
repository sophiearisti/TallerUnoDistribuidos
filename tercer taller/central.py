import socket
import json
import math
import json
import time
import paho.mqtt.client as mqtt

#Address and port information
PORT = 7000
FORMAT = "utf-8"

SERVERC = "192.168.193.148" #COMPU KEVIN
SERVER1 = "192.168.193.144" #COMPU LUISA
SERVER2 = "192.168.193.79"  #COMPU DANIEL
SERVER3 = "192.168.193.150" #VIRTUAL SOPHIA
# "192.168.193.127" VIRTUAL ALANIS (CLIENTE)}  
  
mqttBroker = "mqtt.eclipseprojects.io"
LOCALHOST = socket.gethostbyname(socket.gethostname())

def on_message(client, userdata, message):
    print("Mensaje recibido en el tema:", message.topic)
    print("Contenido del mensaje:", str(message.payload.decode("utf-8")))
    
    # Decodificar el JSON recibido
    json_data = json.loads(message.payload.decode("utf-8"))
    
    # Obtener la respuesta del JSON
    numero1 = json_data["numero1"]
    numero2 = json_data["numero2"]
    topic=json_data["topic"]

    print("Peticion recibida: num1 "+str(numero1)+" num2 "+ str(numero2)+ " IP "+topic)  

    #aqui se le envia de nuevo al broker para que se lo envie al servidor de calculo correspondiente
    res1=enviar_calculo(numero1,numero1,1,"CALCULO",client)

    res2=enviar_calculo(numero2,numero2,2,"CALCULO",client)

    res_final=enviar_calculo(res1,res2,3,"CALCULO",client)


    eviar_respuesta(2,topic,client)

def enviar_calculo(numero1,numero2,tipo,topic,client):
    new_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"CENTRALREQUEST")
    new_client.connect(mqttBroker)
    print("enviando")
    enviar = json.dumps({"numero1": numero1, "numero2": numero2, "topic": LOCALHOST, "tipo": tipo})
    client.publish(topic, enviar)
    enviar_dict = json.loads(enviar)

    print(
        "Publicado: val1 "
        + str(enviar_dict["numero1"]) # Convertir el entero a cadena
        + " val2 "
        + str(enviar_dict["numero2"])
        + " topic "
        + enviar_dict["topic"]
        + " tipo: "
        + str(enviar_dict["tipo"])
        + " al tema CALCULO"
    )

    return 1
        

def eviar_respuesta(res,topic,client):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "CENTRAL")

    client.connect(mqttBroker)

    enviar = json.dumps({"respuesta": res})

    client.publish(topic, enviar)

    # Convertir la cadena JSON de vuelta a un diccionario
    enviar_dict = json.loads(enviar)

    print(
        "publicado: respuesta "
        + str(enviar_dict["respuesta"])
    )

    # Detener el bucle de eventos y desconectar el cliente MQTT
    client.disconnect()
    client.loop_stop()
    print("ESPERANDO OTRA PETICION")

    
#MAIN
print("[ENCENDIENDO] SERVIDOR CENTRAL")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"CENTRAL")
# Asociación de la función de devolución de llamada on_message al cliente MQTT

# Conexión al broker MQTT y suscripción al tema "test/topic"
client.connect(mqttBroker)
client.subscribe("PETICION")

# Inicio del bucle de eventos del cliente MQTT
client.loop_start()
# Bucle principal para mantener el script en ejecución
try:
    while True:
        # Asociación de la función de devolución de llamada on_message al cliente MQTT
        client.on_message = on_message
        #print("esperando")
        time.sleep(1)
except KeyboardInterrupt:
    # Si se interrumpe manualmente el script, detener el bucle de eventos y desconectar el cliente MQTT
    client.disconnect()
    client.loop_stop()