import socketserver
import threading
import socket


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        cur_thread = threading.current_thread()
        data = self.request.recv(1024)
        print(f"current thread: {cur_thread.ident}")
        print(f"server thread {cur_thread.ident} | {self.client_address[0]}:{self.client_address[1]} wrote:\n {data.decode()}")
        self.request.sendall(data.upper())


class AsyncServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # the order very matters
    pass


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 1234
    server = AsyncServer((HOST, PORT), TCPHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print("Server loop running in thread:", server_thread.ident)
