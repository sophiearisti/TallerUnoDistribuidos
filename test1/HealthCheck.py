import zmq
from constants import environment
import threading
import time
from scalene import scalene_profiler

PrincipalActivo = False
lock = threading.Lock()

def main(): 
    threading.Thread(target=manejarPrincipal).start()
    threading.Thread(target=manejarSecundario).start()
    

def manejarPrincipal():
    context = zmq.Context()
    #para primera respuesta del fog
    receiver = context.socket(zmq.REP)
    receiver.bind(f"tcp://{environment.HEALTH_CHECK['host']}:{environment.HEALTH_CHECK['port_1']}")
    result = receiver.recv()
    print("PING RECIBIDO: {result}")
    print(result)
    receiver.send(b"Mensaje recibido por el SC")
    
    #request al principal
    sender = context.socket(zmq.REQ)
    sender.connect(f"tcp://{environment.PROXY_SOCKET['host']}:{environment.PROXY_SOCKET['port']}")
    
    # Establecer un timeout de recepción de 5000 milisegundos (5 segundos)
    sender.setsockopt(zmq.RCVTIMEO, 5000)  # 5000 ms = 5 s
    global PrincipalActivo
    while True:
        try:
            sender.send_string("EXISTES?")
            message = sender.recv_string()
            print(f"Respuesta recibida: {message}")  
            with lock:
                PrincipalActivo = True
            time.sleep(5)
        except zmq.error.Again:
            print("No se recibió respuesta en 5 segundos, reintentando...")
        except zmq.error.ZMQError as e:
            if e.errno == zmq.EFSM:  # Estado incorrecto del socket
                sender.close()
                sender = context.socket(zmq.REQ)
                sender.connect(f"tcp://{environment.PROXY_SOCKET['host']}:{environment.PROXY_SOCKET['port']}")
                sender.setsockopt(zmq.RCVTIMEO, 5000)  # Timeout de 5 segundos para recibir
                with lock:
                    PrincipalActivo = False
                result = receiver.recv()
                print("PING RECIBIDO: {result}")
                print(result)
                receiver.send(b"Mensaje recibido por el SC")
                

def manejarSecundario():
    context = zmq.Context()
    #reply al secundario
    receiver = context.socket(zmq.REP)
    receiver.bind(f"tcp://{environment.HEALTH_CHECK['host']}:{environment.HEALTH_CHECK['port_2']}")

    while True:
        result = receiver.recv()
        print("PROXY2: {result}")
        print(result)
        with lock:
            receiver.send_string(f"{PrincipalActivo}")

if __name__ == "__main__":
    main()