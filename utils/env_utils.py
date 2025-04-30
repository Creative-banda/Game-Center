import os
import getpass
import subprocess
from pygame import mixer
from datetime import datetime
from pathlib import Path


mixer.init()

current_path = Path(__file__).parent.resolve()

camera_click_sound = mixer.Sound(f"{current_path}/sounds/camera_click.mp3")

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



def get_env_for_screenshot():
    env = os.environ.copy()

    # Set specific variables for the normal user (force normal user environment)
    env['USER'] = getpass.getuser()  # Set the normal user name
    env['HOME'] = os.path.expanduser('~')  # Set home directory for the normal user
    env['XDG_RUNTIME_DIR'] = os.environ.get('XDG_RUNTIME_DIR', '/run/user/1000')  # Ensure display access

    return env


def take_screenshot(env):
        
        # Play camera click sound
        camera_click_sound.play()
        
        # Generate a unique filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'screenshot_{timestamp}.png'

        # Full path where screenshot will be saved
        save_path = current_path / 'screenshots' / filename

        # Save the screenshot
        subprocess.run(["grim", str(save_path)], env=env)

        print(f"Screenshot saved as {save_path}")