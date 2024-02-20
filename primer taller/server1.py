import socket
import threading
import json

#Address and port information
PORT = 7000
FORMAT = "utf-8"
SERVER1 = "192.168.193.144"
ADDR1 = (SERVER1,PORT)

#binding the socket to the specific port/ip
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR1)

def start( ):
    server.listen()
    print(f"[ESCUCHANDO] Servidor escuchando en {SERVER1}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn,addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS]  {threading.active_count() -1}")


def handle_client(conn, addr):
    print(f"[CONEXION NUEVA] {addr} conectado.")

    msg = json.loads(conn.recv(1024))    
    print(f"[{addr}] {msg}")
        
    paso = msg["paso"]
    num = msg["numero"]

    print(f"PASO: {paso} NUMERO: {num}")
    num = float(num)
    cuadrado = str(pow(num, 2))

    conn.send(cuadrado.encode(FORMAT))
    print(f"[ENVIADO] {cuadrado}")
    conn.close()

print("[ENCENDIENDO] SERVIDOR CALCULO 1")
start( )

