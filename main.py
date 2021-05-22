import argparse
import time

from ia import IA

HOST = "127.0.0.1"
PORT = 2121

if __name__ == "__main__":

    # Parse arguments: python main.py <host> <port>
    parser = argparse.ArgumentParser()
    parser.add_argument("host", default=HOST)
    parser.add_argument("port", default=PORT, type=int)
    parser.add_argument("-w", default=False, type=bool, nargs="?", const=True)
    args = parser.parse_args()
    host = args.host
    port = args.port
    print(host, port)

    # Wait for server to be launched
    if args.w:
        time.sleep(2)

    ia = IA(host, port)

    while True:
        print("PLAYING")
        if not ia.play():
            break

    print("END")
