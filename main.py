import argparse
import pwn

HOST = "127.0.0.1"
PORT = 12345

if __name__ == "__main__":

    game_on = True

    # Parse arguments: python main.py <host> <port>
    parser = argparse.ArgumentParser()
    parser.add_argument("host", default=HOST)
    parser.add_argument("port", default=PORT, type=int)
    args = parser.parse_args()
    host = args.host
    port = args.port
    print(host, port)

    # Connect to remote server
    r = pwn.remote(host, port)
    # Send a request to server
    r.send("GET /\r\n\r\n")

    # Receive the response
    data = r.recvall()
    print(data.decode())

    while game_on:
        break
