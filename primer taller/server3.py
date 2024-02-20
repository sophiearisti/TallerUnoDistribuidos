import json
import math
import socket
import threading

# Address and port information
PORT = 7000
FORMAT = "utf-8"
SERVER3 = "192.168.193.126"
ADDR3 = (SERVER3, PORT)

# binding the socket to the specific port/ip
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR3)


def start():
    server.listen()
    print(f"[ESCUCHANDO] Servidor escuchando en {SERVER3}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS]  {threading.active_count() -1}")


def handle_client(conn, addr):
    print(f"[CONEXION NUEVA] {addr} conectado.")

    msg = json.loads(conn.recv(1024))
    print(f"[{addr}] {msg}")

    paso = msg["paso"]
    num1 = float(msg["numero1"])
    num2 = float(msg["numero2"])

    print(f"PASO: {paso} NUMERO1: {num1} NUMERO2: {num2}")
    suma = num1 + num2
    hipotenusa = str(math.sqrt(suma))

    conn.send(hipotenusa.encode(FORMAT))
    print(f"[ENVIADO] {hipotenusa}")

    conn.close()


print("[ENCENDIENDO] SERVIDOR CALCULO 3")
start()
