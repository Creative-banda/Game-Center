import os
import sys, subprocess, pathlib

current_path = pathlib.Path(__file__).parent.resolve()

def restart_script():
    """Runs the script again and exits the current one."""    
    print("Restarting script...")
    subprocess.Popen([sys.executable, f"python {current_path}/main.py"])
    sys.exit()  # Exit current script


restart_script()