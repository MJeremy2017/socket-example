import socket
import types
import selectors


messages = [b'message 1', b'message 2']
sel = selectors.DefaultSelector()


def start_connection(host, port, num_conns):
    server_addr = (host, port)
    for i in range(num_conns):
        connid = i+1
        print(f"connection {connid} connect to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum(len(m) for m in messages),
                                     recv_total=0,
                                     messages=list(messages),
                                     outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(sock, events, data)


def service_connection(key, mask):
    # It keeps track of the number of bytes it’s received from the server so it can close its side of the connection.
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)

        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


HOST = '127.0.0.1'
PORT = 6000

while True:
    # It returns a list of (key, events) tuples, one for each socket
    events = sel.select(timeout=None)  # blocks until there are sockets ready for I/O.
    for key, mask in events:
        if key.data is None:
            # then we know it's from the listening socket and we need to accept connections
            start_connection(HOST, PORT, 2)
        else:
            service_connection(key, mask)  # else means it's already been connected
