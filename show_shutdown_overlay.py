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

    label = tk.Label(
        root,
        text="⚠️ Shutting Down...",
        font=("Helvetica", 40, "bold"),
        fg="white",
        bg="#123456"
    )
    label.place(relx=0.5, rely=0.5, anchor="center")

    # Shutdown after 1.5 seconds (same as the overlay close)
    def delayed_shutdown():
        root.destroy()  # Close UI
        os.system("sudo shutdown now")

    root.after(1500, delayed_shutdown)
    root.mainloop()
