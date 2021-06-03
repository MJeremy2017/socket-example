import socketserver
import threading


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        cur_thread = threading.current_thread()
        data = self.request.recv(1024)
        print(f"current server thread: {cur_thread.ident}")
        print(f"{self.client_address[0]}:{self.client_address[1]} wrote:\n {data.decode()}")
        self.request.sendall(data.upper())
        # self.data = self.rfile.readline().strip()
        # self.wfile.write(self.data.upper())


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 1234
    print(f"server starts on {HOST}:{PORT}")
    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        server.serve_forever()