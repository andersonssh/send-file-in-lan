"""
Classes para manipular as conexoes
"""
import socket


class SocketHandler:
    BUFFER_SIZE = 4096

    def __init__(self, host: str, port: int):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = host
        self._port = port


class ClientHandler(SocketHandler):
    """
    Manipular o socket do tipo cliente
    """
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    def send_data(self, data: bytes):
        self._socket.send(data)

    def receive_data(self, buffer_size: int = 0):
        if not buffer_size:
            buffer_size = SocketHandler.BUFFER_SIZE
        return self._socket.recv(buffer_size)

    def connect(self):
        self._socket.connect((self._host, self._port))

    def __repr__(self):
        return f'<ClientHandler addr=("{self._host}", {self._port})>'


class ServerHandler(SocketHandler):
    """
    Manipular o socket do tipo servidor
    """
    def __init__(self, host: str = '0.0.0.0', port: int = 5000):
        super().__init__(host, port)

    def configure(self):
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self._host, self._port))
        self._socket.listen(5)

    def accept(self) -> tuple:
        client_socket, addr = self._socket.accept()
        return client_socket, addr

    @classmethod
    def receive_data(cls, client_socket: socket, buffer_size: int = 0):
        if not buffer_size:
            buffer_size = SocketHandler.BUFFER_SIZE
        return client_socket.recv(buffer_size)

    @classmethod
    def send_data(cls, client_socket: socket, data: bytes):
        client_socket.send(data)

    def __repr__(self):
        return f'<ServerHandler addr=("{self._host}", {self._port})>'
