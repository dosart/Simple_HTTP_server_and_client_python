"""
The simplest possible socket server (blocking).

Works only for one client.
sock.recv() throws an exception on client disconnected.
"""

import socket

from threading import Thread
from typing import Tuple

class Handler(Thread):
    def __init__(self, client_socket: socket.socket):
        """
        Initialize a new handler thread.

        :param client_socket: The socket of the client to serve.
        """
        super().__init__()
        self.client_socket = client_socket
    
    def run(self) -> None:
        """
        Serve a client connection.
        """
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f"Received: {data}")
                message = "OK" 
                self.client_socket.sendall(message.encode())
        except socket.error as e:
            print(f"Error serving client: {e}")
        finally:
            self.client_socket.close()

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
    
    def start(self) -> None:
        """
        Start the server.
        """
        try:
            while True:
                client_socket, client_address = self.accept_client()

                thread = Handler(client_socket)
                thread.start()

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