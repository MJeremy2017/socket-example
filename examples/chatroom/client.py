import socket
import threading
import sys


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print(f"client connected to {self.host}:{self.port}")

    def run(self):
        while True:
            thread_recv = threading.Thread(target=self.receive)
            thread_recv.start()

            message = sys.stdin.readline()[:-1]
            message = message.encode()
            print(message)
            self.sock.sendall(message)

    def receive(self):
        while True:
            data = self.sock.recv(1024)
            if data:
                print(repr(data))
            else:
                break


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('server')
    parser.add_argument('--host', default='localhost', help='server host')
    parser.add_argument('--port', type=int, default=1234, help='server port')
    args = parser.parse_args()

    HOST = args.host
    PORT = args.port
    print(f"server starts on {HOST}:{PORT}")

    c = Client(HOST, PORT)
    c.run()


