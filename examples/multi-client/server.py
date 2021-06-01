import selectors
import socket
import types

HOST = '127.0.0.1'
PORT = 6000


def accept_wrapper(sock):
    conn, address = sock.accept()
    print('connected on address', address)
    conn.setblocking(False)
    # create an object to store data
    data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)  # register the new socket(conn) for read and write events


def service_connection(key, mask):
    # mask contains the events that are ready.
    sock = key.fileobj
    data = key.data
    # If the socket is ready for reading, then mask & selectors.EVENT_READ is true
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f'send data {repr(data.outb)} to address {data.addr}')
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


sel = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
lsock.setblocking(False)

# sel.register() registers the socket to be monitored with sel.select() for the events you’re interested in.
sel.register(lsock, selectors.EVENT_READ, data=None)

while True:
    # It returns a list of (key, events) tuples, one for each socket
    events = sel.select(timeout=None)  # blocks until there are sockets ready for I/O.
    for key, mask in events:
        if key.data is None:
            # then we know it's from the listening socket and we need to accept connections
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)  # else means it's already been connected
