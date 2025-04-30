import os
import getpass
import subprocess

def get_actual_user():
    return os.getenv("SUDO_USER") or getpass.getuser()

def get_display_env():
    env = os.environ.copy()
    user = get_actual_user()
    home = os.path.expanduser(f"~{user}")

    env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
    env["XAUTHORITY"] = f"{home}/.Xauthority"
    env["USER"] = user
    env["HOME"] = home
    env["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"

    return env, user

