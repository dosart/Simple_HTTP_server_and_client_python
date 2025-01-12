"""
A simple blocking socket server.

This server accepts a single client connection at a time and blocks
while waiting for data from the client. When the client disconnects,
sock.recv() throws an exception.

Classes:
    Server:
        Manages the socket server operations, including accepting and serving
        a client connection.

Methods:
    Server.__init__(self, host: str, port: int):
        Initializes a new socket server with the specified host and port.
    Server.accept_client(self) -> Tuple[socket.socket, Tuple[str, int]]:
        Accepts a new client connection and returns the connected socket and the client address.
    Server.serve(self, client_socket: socket.socket) -> None:
        Handles data transmission for the client connection.
    Server.start(self) -> None:
        Starts the server and continuously accepts and serves client connections.

Attributes:
    HOST (str): Symbolic name meaning all available interfaces.
    PORT (int): Arbitrary non-privileged port.
"""

import socket
from typing import Tuple

class Server:
    def __init__(self, host: str, port: int):
        """
        Initialize a new socket server.

        :param host: The hostname or IP address to bind to.
        :param port: The port number to listen on.
        """
        self.host = host
        self.port = port

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print(f"Server started on {self.host}:{self.port}")
        except OSError as e:
            print(f"Error starting server: {e}")
            self.server_socket.close()

    def accept_client(self) -> Tuple[socket.socket, Tuple[str, int]]:
        """
        Accept a new client connection.

        :return: The connected socket and the address of the client.
        """
        try:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connected by {client_address}")
            return client_socket, client_address
        except socket.error as e:
            print(f"Error accepting client connection: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def serve(self, client_socket: socket.socket) -> None:
        """
        Serve a client connection.

        :param client_socket: The socket of the client to serve.
        """
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received: {data}")
                message = "OK"
                client_socket.sendall(message.encode())
        except socket.error as e:
            print(f"Error serving client: {e}")
        finally:
            client_socket.close()

    def start(self) -> None:
        """
        Start the server.
        """
        try:
            while True:
                client_socket, client_address = self.accept_client()
                self.serve(client_socket)
        except KeyboardInterrupt:
            print("Server stopped")
        finally:
            self.server_socket.close()

# HOST = socket.gethostname()  # Make socket visible to outside world
# HOST = "localhost"  # or "127.0.0.1" visible only within same machine
HOST = ""  # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port

if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.start()
