import argparse
import time

from network import *

HOST = "127.0.0.1"
PORT = 2121
TEAM_NAME = "DogeTeam"
BOARD_SIZE = 31

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

    c = Connection(host, port)
    cmd, = c.receive_command()
    if cmd == ServerCmd.NAME:
        c.send_raw(TEAM_NAME)
    else:
        print("PAS ouf")

    num = -1
    wait = True
    while wait:
        cmd, num = c.receive_command()
        if cmd == ServerCmd.START:
            wait = False
        else:
            print("WARNING: Received another message ({}) before START!".format(cmd))

    print("Started as team number {}!".format(num))
    c.send(Cmd.GETMAP)
    cmd, board_raw = c.receive_command()
    board = [[" " for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            board[y][x] = board_raw[y * BOARD_SIZE + x]

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            print(board[y][x], end=" ")
        print()

    while game_on:
        break
