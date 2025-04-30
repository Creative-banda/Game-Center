import customtkinter as ctk
import os
import time
import threading

def show_shutdown():
    # Set theme and appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Create main window
    root = ctk.CTk()
    root.title("Shutting Down")
    root.overrideredirect(True)
    root.wm_attributes("-topmost", True)
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    
    # Create a frame to hold content
    main_frame = ctk.CTkFrame(root, fg_color="#101010", corner_radius=0)
    main_frame.pack(fill="both", expand=True)
    
    # Gaming console logo placeholder (you can replace with a real logo)
    logo_frame = ctk.CTkFrame(main_frame, fg_color="#101010", height=80, width=80, corner_radius=15)
    logo_frame.place(relx=0.5, rely=0.35, anchor="center")
    
    logo_label = ctk.CTkLabel(
        logo_frame, 
        text="🎮", 
        font=ctk.CTkFont(family="Arial", size=50),
        text_color="#00ffcc"
    )
    logo_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # Main Shutdown Text
    title_label = ctk.CTkLabel(
        main_frame,
        text="POWERING OFF",
        font=ctk.CTkFont(family="Helvetica", size=25, weight="bold"),
        text_color="#00ffcc"
    )
    title_label.place(relx=0.5, rely=0.48, anchor="center")
    
    # Subtext
    sub_label = ctk.CTkLabel(
        main_frame,
        text="Please wait while your console shuts down",
        font=ctk.CTkFont(family="Helvetica", size=10),
        text_color="#888888"
    )
    sub_label.place(relx=0.5, rely=0.54, anchor="center")
    
    # Cancel instruction text
    cancel_text = ctk.CTkLabel(
        main_frame,
        text="Press SPACE to cancel",
        font=ctk.CTkFont(family="Helvetica", size=10),
        text_color="#666666"
    )
    cancel_text.place(relx=0.5, rely=0.59, anchor="center")
    
    # Create progress bar
    progress_bar = ctk.CTkProgressBar(
        main_frame, 
        width=300, 
        height=10, 
        corner_radius=5,
        progress_color="#00ffcc"
    )
    progress_bar.place(relx=0.5, rely=0.63, anchor="center")
    progress_bar.set(0)
    
    # Create glowing effect for the logo
    def animate_glow():
        alpha = 0
        increasing = True
        while True:
            if increasing:
                alpha += 0.03
                if alpha >= 1:
                    alpha = 1
                    increasing = False
            else:
                alpha -= 0.03
                if alpha <= 0.4:
                    alpha = 0.4
                    increasing = True
                    
            # Map alpha (0-1) to font size (45-55)
            size = int(25 + alpha * 10)
            logo_label.configure(font=ctk.CTkFont(family="Arial", size=size))
            time.sleep(0.05)
    
    # Function to fill progress bar
    def fill_progress_bar():
        progress = 0
        while progress < 1:
            progress += 0.05
            progress_bar.set(progress)
            time.sleep(0.035)
        
        # When progress bar finishes, actually shut down
        root.after(500, delayed_shutdown)
    
    # Start animations in separate threads
    threading.Thread(target=animate_glow, daemon=True).start()
    threading.Thread(target=fill_progress_bar, daemon=True).start()
    
    # Function to handle shutdown
    def delayed_shutdown():
        root.destroy()
        os.system("sudo shutdown now")
    
    # Small system status text at bottom
    status_label = ctk.CTkLabel(
        main_frame,
        text="SAVING SYSTEM STATE • CLEARING CACHE • FINALIZING",
        font=ctk.CTkFont(family="Helvetica", size=10),
        text_color="#555555"
    )
    status_label.place(relx=0.5, rely=0.85, anchor="center")
    
    # Add a button to cancel shutdown (optional)
    def cancel_shutdown(event=None):
        root.destroy()
    
    cancel_button = ctk.CTkButton(
        main_frame,
        text="CANCEL",
        font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
        fg_color="#222222",
        text_color="#888888",
        hover_color="#333333",
        width=100,
        height=30,
        corner_radius=5, 
        command=cancel_shutdown
    )
    cancel_button.place(relx=0.5, rely=0.72, anchor="center")
    
    # Use escape key to cancel shutdown
    root.bind("<space>", lambda event: cancel_shutdown())
    
    root.mainloop()

if __name__ == "__main__":
    try:
        show_shutdown()
    except Exception as e:
        print(f"Error: {e}")
        # Fallback shutdown if UI fails
        os.system("sudo shutdown now")