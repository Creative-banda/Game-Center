import tkinter as tk

from datetime import datetime
from pathlib import Path
import subprocess
from pygame import mixer
from utils.env_utils import get_display_env
mixer.init()


env, user = get_display_env()



current_path = Path(__file__).parent.resolve()

camera_click_sound = mixer.Sound(f"{current_path}/sounds/camera_click.mp3")

def show_screenshot_popup():
    popup = tk.Tk()
    popup.overrideredirect(True)  # Remove window border
    popup.attributes("-topmost", True)
    popup.configure(bg="#101010")  # Background color

    # --- Popup Size ---
    width = 400
    height = 80

    # --- Get Screen Width ---
    screen_width = popup.winfo_screenwidth()

    # --- Calculate x and y coordinates ---
    x = (screen_width // 2) - (width // 2)
    y = 50  # 50px from the top

    popup.geometry(f"{width}x{height}+{x}+{y}")

    message = tk.Label(
        popup,
        text="📸 Screenshot Saved Successfully!",
        font=("Orbitron", 14, "bold"),
        fg="#00ffcc",
        bg="#101010",
        padx=20,
        pady=20
    )
    message.pack(fill="both", expand=True)

    # --- Auto Close after 1.5 seconds ---
    popup.after(1000, popup.destroy)

    popup.mainloop()


def take_screenshot():
        
        # Play camera click sound
        camera_click_sound.play()
        

        # Generate a unique filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'screenshot_{timestamp}.png'

        # Full path where screenshot will be saved
        save_path = current_path / 'screenshots' / filename

        # Save the screenshot
        subprocess.run(["sudo", "-u", user, "grim", str(save_path)], env=env, check=True)


        print(f"Screenshot saved as {save_path}")
        
        show_screenshot_popup()


if __name__ == "__main__":
    take_screenshot()