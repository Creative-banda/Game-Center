import os
import getpass
import subprocess
from pygame import mixer
from datetime import datetime
from pathlib import Path

mixer.init()

current_path = Path(__file__).parent.parent.resolve()

camera_click_sound = mixer.Sound(f"{current_path}/sounds/camera_click.mp3")

def get_actual_user():
    return os.getenv("SUDO_USER") or getpass.getuser()

def get_display_env():
    env = os.environ.copy()
    
    # Get the actual desktop user
    actual_user = get_actual_user()
    home_dir = os.path.expanduser(f"~{actual_user}")

    env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
    env["XAUTHORITY"] = os.environ.get("XAUTHORITY", f"{home_dir}/.Xauthority")
    env["USER"] = actual_user
    env["HOME"] = home_dir
    env["XDG_RUNTIME_DIR"] = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/1000")  # Hardcode UID for orchids
    env["PULSE_SERVER"] = os.environ.get("PULSE_SERVER", f"/run/user/1000/pulse/native")  # Add PulseAudio

    return env, actual_user

def get_env_for_screenshot():
    env = os.environ.copy()

    # Set specific variables for the orchids user
    env["USER"] = "orchids"  # Explicitly set to orchids
    env["HOME"] = "/home/orchids"
    env["DISPLAY"] = os.environ.get("DISPLAY", ":0")
    env["XAUTHORITY"] = os.environ.get("XAUTHORITY", "/home/orchids/.Xauthority")
    env["XDG_RUNTIME_DIR"] = os.environ.get("XDG_RUNTIME_DIR", "/run/user/1000")
    env["PULSE_SERVER"] = os.environ.get("PULSE_SERVER", "/run/user/1000/pulse/native")

    return env

def take_screenshot(env):
    # Play camera click sound
    camera_click_sound.play()
    
    # Generate a unique filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"

    # Full path where screenshot will be saved
    save_path = current_path / "screenshots" / filename

    # Ensure screenshots directory exists
    (current_path / "screenshots").mkdir(exist_ok=True)

    # Save the screenshot using scrot (X-compatible)
    try:
        subprocess.run(["scrot", str(save_path)], env=env, check=True)
        print(f"Screenshot saved as {save_path}")
    except subprocess.CalledProcessError as e:
        print(f"Screenshot failed: {e}")
    except FileNotFoundError:
        print("Error: scrot not found. Please install it with 'sudo apt install scrot'.")

# Example usage (if called directly)
if __name__ == "__main__":
    env, user = get_display_env()
    take_screenshot(env)