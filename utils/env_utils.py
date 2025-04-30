import os
import getpass
import subprocess

def get_actual_user():
    return os.getenv("SUDO_USER") or getpass.getuser()

def get_display_env():
    env = os.environ.copy()
    
    # Get the actual desktop user, even when running via sudo
    actual_user = os.getenv("SUDO_USER") or getpass.getuser()
    home_dir = os.path.expanduser(f"~{actual_user}")

    env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
    env["XAUTHORITY"] = os.environ.get("XAUTHORITY", f"{home_dir}/.Xauthority")
    env["USER"] = actual_user
    env["HOME"] = home_dir
    env["XDG_RUNTIME_DIR"] = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")

    return env, actual_user

