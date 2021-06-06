import socket
import threading
import argparse


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connections = []

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen()

        while True:
            sub_sock, address = sock.accept()
            print("server connected on", address)
            # new thread
            ss = ServerSocket(sub_sock, address, self.connections)
            ss.start()
            self.connections.append(sub_sock)


class ServerSocket(threading.Thread):
    def __init__(self, sock: socket, address, connections):
        super().__init__()
        self.sock: socket = sock
        self.address = address
        self.thread_id = threading.current_thread().ident
        self.connections = connections

    def run(self) -> None:
        while True:
            data = self.sock.recv(1024)
            print(f"{self.thread_id}: received data {data}")
            if data:
                self.broadcast(data)
            else:
                print(f"connection on address {self.address} break")
                break

    def broadcast(self, data) -> None:
        for conn in self.connections:
            # send data to other users
            if conn != self.sock:
                # print(f"send data {data} to {conn.getpeername()}")
                message = f"{self.address[0]}:{self.address[1]} said: {data.decode()}"
                message = message.encode()
                conn.sendall(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('server')
    parser.add_argument('--host', default='localhost', help='server host')
    parser.add_argument('--port', type=int, default=1234, help='server port')
    args = parser.parse_args()

    HOST = args.host
    PORT = args.port
    print(f"server starts on {HOST}:{PORT}")
    server = Server(args.host, args.port)
    server.run()

