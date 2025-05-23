import tkinter as tk

from utils.env_utils import get_display_env


env, _ = get_display_env()


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

        
if __name__ == "__main__":
    show_screenshot_popup()