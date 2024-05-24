import asyncio
import zmq.asyncio
from constants import environment

async def run_proxy():
    context = zmq.asyncio.Context()

    # Creating subX interface
    subX = context.socket(zmq.SUB)
    subX.bind(f'tcp://*:{environment.BROKER_SOCKET["sub_port"]}')
    subX.setsockopt_string(zmq.SUBSCRIBE, "")

    # Creating the pubX interface
    pubX = context.socket(zmq.PUB)
    pubX.bind(f'tcp://*:{environment.BROKER_SOCKET["pub_port"]}')

    print("Proxy is active!")

    try:
        # connect subX and pubX (creating the proxy)
        zmq.proxy(subX, pubX)
    except Exception as e:
        print(f"Proxy error: {e}")
    finally:
        # close and free resources
        subX.close()
        pubX.close()
        context.term()

if __name__ == "__main__":
    asyncio.run(run_proxy())
