import asyncio

import zmq

from constants import environment


async def run() -> None:
    # Creating zmq context
    context = zmq.Context()

    # Creating subX interface
    subX = context.socket(zmq.SUB)
    subX.bind(f'tcp://*:{environment.BROKER_SOCKET["sub_port"]}')

    subX.setsockopt_string(zmq.SUBSCRIBE, "")

    # Creating the pubX interface
    pubX = context.socket(zmq.PUB)
    pubX.bind(f"tcp://*:{environment.BROKER_SOCKET["pub_port"]}")

    print("Proxy is active!")
    # connect subX and pubX (creating the proxy)
    zmq.device(zmq.FORWARDER, subX, pubX)

    # close and free resources
    subX.close()
    pubX.close()
    context.term()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
