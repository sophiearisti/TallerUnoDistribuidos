import socket
import json

SERVERC = "192.168.193.148"
PORT = 7000
FORMAT = "utf-8"
ADDR = (SERVERC,PORT)

print("Ingresa los el valor de los catetos para calcular la hipotenusa")
numero1=input("Ingresa el valor del primer cateto:")
numero2=input("Ingresa el valor del segundo cateto:")

enviar=json.dumps({"numero1":numero1,"numero2":numero2})

peticion = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
peticion.connect(ADDR)

peticion.send(enviar.encode(FORMAT))

respuesta = peticion.recv(1024).decode(FORMAT)
print ("el valor de la hipotenusa es:", respuesta)