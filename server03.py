"""
A simple blocking socket server using processes for handling connections.

This server accepts client connections and spawns a new process for each client
to handle data transmission. The use of processes helps to avoid blocking the 
main server loop, allowing multiple clients to be served concurrently.

Functions:
    handle_connection(sock, addr):
        Handles the data received from the client and processes it.

Main Execution:
    Initializes and starts the server to accept client connections.

Attributes:
    HOST (str): Symbolic name meaning all available interfaces.
    PORT (int): Arbitrary non-privileged port.
"""

import socket
import multiprocessing

def handle_connection(sock, addr):
    """
    Handle the client connection.

    :param sock: Client socket
    :param addr: Client address
    """
    with sock:
        print("Connected by", addr)
        while True:
            # Receive data from client
            try:
                data = sock.recv(1024)
            except ConnectionError:
                print(f"Client suddenly closed while receiving")
                break
            print(f"Received: {data} from: {addr}")
            if not data:
                break

            # Process data
            if data == b"close":
                break
            data = data.upper()

            # Send data back to client
            print(f"Send: {data} to: {addr}")
            try:
                sock.sendall(data)
            except ConnectionError:
                print(f"Client suddenly closed, cannot send")
                break
        print("Disconnected by", addr)

HOST = ""  # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock