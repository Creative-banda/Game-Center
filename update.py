import os
import sys, subprocess, pathlib

current_path = pathlib.Path(__file__).parent.resolve()

def restart_script(self):
    """Runs the script again and exits the current one."""    
    subprocess.Popen([sys.executable, f"{current_path}/main.py"])
    sys.exit()  # Exit current script

