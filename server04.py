"""
A non-blocking socket server using selectors and a callback system.

This server accepts and manages multiple client connections concurrently
by utilizing the selectors module. Callbacks are used to handle new connections,
data reception, and disconnections.

Functions:
    on_connect(sock, addr):
        Callback invoked when a new client connects.
    on_disconnect(sock, addr):
        Callback invoked when a client disconnects.
    handle(sock, addr):
        Handles data received from the client and processes it.

Functions in run_server:
    on_accept_ready(sel, serv_sock, mask):
        Handles new incoming client connections.
    on_read_ready(sel, sock, mask):
        Handles data read events for a connected client socket.

Methods:
    run_server(host, port, on_connect, on_read, on_disconnect):
        Runs the socket server with specified host, port, and callbacks.

Attributes:
    HOST (str): Symbolic name meaning all available interfaces.
    PORT (int): Arbitrary non-privileged port.
"""

import selectors
import socket


def on_connect(sock, addr):
    """
    Callback invoked when a new client connects.

    :param sock: Client socket
    :param addr: Client address
    """
    print("Connected by", addr)


def on_disconnect(sock, addr):
    """
    Callback invoked when a client disconnects.

    :param sock: Client socket
    :param addr: Client address
    """
    print("Disconnected by", addr)


def handle(sock, addr):
    """
    Handle data received from client.

    :param sock: Client socket
    :param addr: Client address
    :return: True if connection should remain open, False otherwise
    """
    try:
        data = sock.recv(1024)  # Should be ready
    except ConnectionError:
        print(f"Client suddenly closed while receiving")
        return False

    print(f"Received {data} from: {addr}")

    if not data:
        print("Disconnected by", addr)
        return False

    # Process data
    if data == b"close":
        return False

    data = data.upper()

    # Send data back to client
    print(f"Send: {data} to: {addr}")
    try:
        sock.send(data)  # Hope it won't block
    except ConnectionError:
        print(f"Client suddenly closed, cannot send")
        return False

    return True


def run_server(host, port, on_connect, on_read, on_disconnect):
    """
    Run the socket server.

    :param host: Hostname or IP address
    :param port: Port number
    :param on_connect: Callback for new connections
    :param on_read: Callback for reading data
    :param on_disconnect: Callback for disconnecting clients
    """

    def on_accept_ready(sel, serv_sock, mask):
        sock, addr = serv_sock.accept()  # Should be ready
        sock.setblocking(False)
        sel.register(sock, selectors.EVENT_READ, on_read_ready)
        if on_connect:
            on_connect(sock, addr)

    def on_read_ready(sel, sock, mask):
        addr = sock.getpeername()
        if not on_read or not on_read(sock, addr):
            if on_disconnect:
                on_disconnect(sock, addr)
            sel.unregister(sock)
            sock.close()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
            serv_sock.bind((host, port))
            serv_sock.listen(1)
            serv_sock.setblocking(False)
            sel = selectors.DefaultSelector()
            sel.register(serv_sock, selectors.EVENT_READ, on_accept_ready)

            while True:
                print("Waiting for connections or data...")
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(sel, key.fileobj, mask)

    except Exception as e:
        print(f"Server error: {e}")


HOST = ""  # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port

if __name__ == "__main__":
    run_server(HOST, PORT, on_connect, handle, on_disconnect)
