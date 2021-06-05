import socketserver


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = self.request[0]
        socket = self.request[1]
        print(f"{self.client_address[0]}:{self.client_address[1]} wrote:\n {data.decode()}")
        socket.sendto(data.upper(), self.client_address)


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 1234
    print(f"server starts on {HOST}:{PORT}")
    with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
        server.serve_forever()