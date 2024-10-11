import socket
from modules.color import Color
import signal


class Server:
    def __init__(self, host, port: int):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.server.settimeout(1)
        self.running = True

        signal.signal(signal.SIGINT, self.signal_handler)

        print(f"{Color.OKGREEN}[*]{Color.DEFAULT} Listening on {self.host}:{self.port}")

    def signal_handler(self, signum, frame):
        print(f"\n{Color.OKGREEN}[*]{Color.DEFAULT} Caught Ctrl+C, shutting down...")
        self.running = False

    def accept(self):
        try:
            client_socket, addr = self.server.accept()
            print(
                f"{Color.OKGREEN}[*]{Color.DEFAULT} Accepted connection from {addr[0]}:{addr[1]}"
            )
            return client_socket
        except socket.timeout:
            return None

    def send(self, client_socket, data):
        if self.running and client_socket:
            try:
                client_socket.send(data)
            except socket.error as e:
                print(f"{Color.FAIL}[!]{Color.DEFAULT} Error sending data: {e}")

    def close(self):
        if self.server:
            self.server.close()
        print(f"{Color.OKGREEN}[*]{Color.DEFAULT} Server closed")


class Session:
    def __init__(self, host, port):
        self.server = Server(host, port)
        self.client_socket = None

    def start(self):
        try:
            while self.server.running:

                if not self.client_socket:
                    self.client_socket = self.server.accept()
                    if not self.client_socket:
                        continue

                signal.signal(signal.SIGINT, signal.SIG_DFL)

                print(f"{Color.OKCYAN}shell>{Color.DEFAULT} ", end="", flush=True)
                command = input()

                if command.lower() == "exit":
                    break

                self.server.send(self.client_socket, command.encode())

                try:
                    response = self.client_socket.recv(6000).decode()
                    print(response)
                except socket.timeout:
                    print(f"{Color.WARNING}[!]{Color.DEFAULT} No response from client")
                except socket.error as e:
                    print(f"{Color.FAIL}[!]{Color.DEFAULT} Error receiving data: {e}")
                    self.client_socket = None

        except KeyboardInterrupt:
            print(
                f"\n{Color.OKGREEN}[*]{Color.DEFAULT} Caught KeyboardInterrupt in Session"
            )
        finally:
            if self.client_socket:
                self.client_socket.close()
            self.server.close()
