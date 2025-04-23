import tkinter as tk
import os

def show_shutdown():
    root = tk.Tk()
    root.title("Shutting Down")
    root.overrideredirect(True)
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "#123456")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.configure(bg="#123456")

    # Base font settings
    font_main = ("Segoe UI", 40, "bold")
    font_sub = ("Segoe UI", 14, "italic")

    # Main label
    label = tk.Label(
        root,
        text="⚠️ Shutting Down...",
        font=font_main,
        fg="white",
        bg="#123456"
    )
    label.place(relx=0.5, rely=0.45, anchor="center")

    # Sub label with glow hint
    sub_label = tk.Label(
        root,
        text="Please wait...",
        font=font_sub,
        fg="#aaa",
        bg="#123456"
    )
    sub_label.place(relx=0.5, rely=0.55, anchor="center")

    # Animate glow effect
    def pulse(count=0):
        # Change color intensity every few ticks to simulate glowing
        glow_colors = ["#ffffff", "#dddddd", "#bbbbbb", "#dddddd"]
        label.config(fg=glow_colors[count % len(glow_colors)])
        root.after(200, lambda: pulse(count + 1))

    pulse()  # Start animation

    # After 1.5 seconds → Shutdown
    def delayed_shutdown():
        root.destroy()
        os.system("sudo shutdown now")

    root.after(1500, delayed_shutdown)
    root.mainloop()

