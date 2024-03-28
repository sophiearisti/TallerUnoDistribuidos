import time 
import zmq

def inicializar():
    ip="192.168.193.79"
    context = zmq.Context()
    # Socket to receive messages on
    receiver = context.socket (zmq.PULL)
    receiver.bind(f"tcp://{ip}:5558")
    # Wait for start of batch
    #S = receiver.recv()
    # Start our clock now
    #tstart = time.time()
    while True:
        result = receiver.recv_json()
        print(f"resultado recibido: {result}")
        
        #if collecter_data.has_key(result['consumer']):
        time.sleep(6)

inicializar()