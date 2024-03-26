import socket
import threading
import math
import sys

def start( ):
    print(f"INICIALIZANDO LOS SENSORES")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn,addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS]  {threading.active_count() -1}")


def create_sensor(conn, addr):
    print(f"[CONEXION NUEVA] {addr} conectado.")

    msg = json.loads(conn.recv(1024))    
        
    num1 = msg["numero1"]
    num2 = msg["numero2"]

    #paso1
    enviar = json.dumps({"paso":1,"numero":num1})
    
    calc1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    calc1.settimeout(TIMEOUT)
    
    try:
        calc1.connect(ADDR1)
        calc1.send(enviar.encode(FORMAT))
        print(f"[ENVIADO] PASO 1| NUM: {num1} a {ADDR1}")
        res1 = calc1.recv(1024).decode(FORMAT)
        res1 = float(res1) #Se convierte
        print(f"[RECIBIDO] Numero 1: {res1} de {ADDR1}")
    except socket.timeout:
        print(f"[FALLO] Servidor {ADDR1}")
        res1 = pow(float(num1),2)
    
    #paso2
    enviar = json.dumps({"paso":2,"numero":num2})
    
    calc2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    calc2.settimeout(TIMEOUT)

    try:
        calc2.connect(ADDR2)
        calc2.send(enviar.encode(FORMAT))
        print(f"[ENVIADO] PASO 2| NUM: {num2} a {ADDR2}")
        res2 = calc2.recv(1024).decode(FORMAT)
        res2 = float(res2) #Se convierte
        print(f"[RECIBIDO] Numero 2: {res2} de {ADDR2}")
    except socket.timeout:
        print(f"[FALLO] Servidor {ADDR2}")
        res2 = pow(float(num2),2)
        
 
    #paso3
    enviar = json.dumps({"paso":3,"numero1":res1, "numero2":res2})
    
    calc3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    calc3.settimeout(TIMEOUT)
    
    try:
        calc3.connect(ADDR3)
        calc3.send(enviar.encode(FORMAT))
        print(f"[ENVIADO] PASO 3| NUM1: {res1} NUM2: {res2} a {ADDR3}")
        res3 = calc3.recv(1024).decode(FORMAT)
        print(f"[RECIBIDO] Numero 2: {res3} de {ADDR3}")
    except socket.timeout:
        print(f"[FALLO] Servidor {ADDR3}")
        suma = float(res1)+float(res2)
        res3 = str(math.sqrt(suma))

    #enviar la respuesta al cliente
    print(f"[ENVIADO] RESULTADO: {res3} a {addr}")
    conn.send(res3.encode(FORMAT))

    #Cerrar la conexion
    conn.close()
    
    
#MAIN
print("[ENCENDIENDO]")
start( )

