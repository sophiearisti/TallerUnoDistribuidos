import zmq

from constants import environment

def run_broker():
    context = zmq.Context()

    # Creating subX interface
    subX = context.socket(zmq.XSUB)
    subX.bind(f'tcp://*:{environment.BROKER_SOCKET["sub_port"]}')


    # Creating the pubX interface
    pubX = context.socket(zmq.XPUB)
    pubX.bind(f'tcp://*:{environment.BROKER_SOCKET["pub_port"]}')

    print("Broker is active!")

    zmq.proxy(subX, pubX)
    
    subX.close()
    pubX.close()
    context.term()

if __name__ == "__main__":
    run_broker()
