import socket
import threading
PORT = 7000
FORMAT = "utf-8"
SERVER = "192.182.193.148"
ADDR = (SERVER,PORT)
DISCONNECT_MESSAGE = "DESCONECTAR"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def start( ):
    server.listen()
    print(f"[ESCUCHANDO] Servidor escuchando en {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn,addr))
        thread.start()
        print(f"[CONNECCIONES ACTIVAS] {threading.active_count() -1}")

def handle_client(conn, addr):
    print(f"[CONNECCION NUEVA] {addr} connectado.")

    connected = True
    while connected:
        msg = conn.recieve(1024).decode(FORMAT)
        print(f"[{addr}] {msg}")
        conn.send("RECIBIDO".encode(FORMAT))
        if msg == DISCONNECT_MESSAGE:
            connected = False
    conn.close()
    
    

print("[ENCENDIENDO]")
start( )

