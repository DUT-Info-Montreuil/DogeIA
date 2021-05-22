import argparse
import time

from structure.client import Client

HOST = "127.0.0.1"
PORT = 2121

if __name__ == "__main__":

    game_on = True

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

    c = Client(host, port)
    num = c.start()
    print(f"Started as team number {num}!")
    board = c.map
    board.print()

    while game_on:
        break
