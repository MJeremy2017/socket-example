import socket
import time
import threading

HOST = '127.0.0.1'
PORT = 1234
cnt = 1

while True:
    data = 'hello world'
    data += str(cnt)
    data += '\n'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(data))
        recv_msg = s.recv(1024).decode()
    print(f"current client thread {threading.current_thread().ident}")
    print(f"sent {data}")
    print(f"received {recv_msg}")
    cnt += 1
    time.sleep(1)
