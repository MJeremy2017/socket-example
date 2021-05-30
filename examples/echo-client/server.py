import socket

HOST = '127.0.0.1'
PORT = 6000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    # accept() blocks and waits for an incoming connection
    # returns a new socket that is used to communicate with the client which is distinct from the
    # listening socket that the server is using to accept new connections
    conn, address = s.accept()  # the address is the client's IP and TCP port
    with conn:
        print("Connected on", address)
        while True:
            data = conn.recv(1024)  # 1024 is buffer size
            if not data:
                break
            conn.sendall(data)
print("server connection closed")