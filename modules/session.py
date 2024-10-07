import socket
from modules.color import Color


class Server:
    def __init__(self, host, port: int):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"{Color.OKGREEN}[*]{Color.DEFAULT} Listening on {self.host}:{self.port}")

    def accept(self):
        client_socket, addr = self.server.accept()
        print(f"{Color.OKGREEN}[*]{Color.DEFAULT} Accepted connection from {addr[0]}:{addr[1]}")
        return client_socket

    def send(self, client_socket, data):
        client_socket.send(data)


class Session:
    def __init__(self, host, port):
        self.server = Server(host, port)
        self.client_socket = self.server.accept()

    def start(self):
        while True:
            if self.client_socket is None:
                continue

            print("shell> ", end="")
            command = input()

            self.server.send(self.client_socket, command.encode())
            print(self.client_socket.recv(6000).decode())
