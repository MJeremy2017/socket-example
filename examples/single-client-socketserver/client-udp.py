import socket
import time

HOST = '127.0.0.1'
PORT = 1234
cnt = 1

while True:
    data = 'hello world'
    data += str(cnt)
    data += '\n'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # no connection required
        s.sendto(str.encode(data), (HOST, PORT))
        recv_msg = s.recv(1024).decode()
    print(f"sent {data}")
    print(f"received {recv_msg}")
    cnt += 1
    time.sleep(1)
