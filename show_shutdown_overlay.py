import tkinter as tk
import os

def show_shutdown():
    root = tk.Tk()
    root.title("Shutting Down")
    root.overrideredirect(True)
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "#101010")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.configure(bg="#101010")

    # --- Fonts ---
    font_main = ("Orbitron", 32, "bold") 
    font_sub = ("Orbitron", 14, "normal")

    # --- Center Icon (text-based emoji style) ---
    icon_label = tk.Label(
        root,
        text="🕹️",
        font=("Arial", 60),
        fg="#00ffcc",
        bg="#101010"
    )
    icon_label.place(relx=0.5, rely=0.35, anchor="center")

    # --- Main Shutdown Text ---
    label = tk.Label(
        root,
        text="Powering Off...",
        font=font_main,
        fg="#00ffcc",
        bg="#101010"
    )
    label.place(relx=0.5, rely=0.48, anchor="center")

    # --- Subtext with pixel style ---
    sub_label = tk.Label(
        root,
        text="Please wait while your console shuts down.",
        font=font_sub,
        fg="#888888",
        bg="#101010"
    )
    sub_label.place(relx=0.5, rely=0.56, anchor="center")

    # --- Pixel-style loading dots ---
    loading_dots = tk.Label(
        root,
        text=".",
        font=font_main,
        fg="#00ffcc",
        bg="#101010"
    )
    loading_dots.place(relx=0.5, rely=0.63, anchor="center")

    def animate_dots(count=0):
        dots = "." * ((count % 3) + 1)
        loading_dots.config(text=dots)
        root.after(300, lambda: animate_dots(count + 1))

    animate_dots()

    # --- Shutdown command after delay ---
    def delayed_shutdown():
        root.destroy()
        os.system("sudo shutdown now")

    root.after(2500, delayed_shutdown)
    root.mainloop()

if __name__ == "__main__":
    # Show the shutdown overlay
    show_shutdown()