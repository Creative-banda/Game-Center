import customtkinter as ctk
from PIL import Image
import time
import threading
import socket
import subprocess
from utils.env_utils import current_path

class SplashScreen(ctk.CTkFrame):
    def __init__(self, master, on_close):
        super().__init__(master, fg_color="#000000")
        self.master = master
        self.on_close = on_close
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.setup_ui()
        self.master.after(100, self.start_animation_and_updates)

    def setup_ui(self):
        # Create a center content container
        self.splash_content = ctk.CTkFrame(self, fg_color="#000000")
        self.splash_content.place(relx=0.5, rely=0.5, anchor="center")

        # Stylish logo
        image_size = min(self.master.winfo_screenwidth(), self.master.winfo_screenheight()) * 0.7
        self.logo_image = ctk.CTkImage(
            dark_image=Image.open(f"{current_path}/assets/logo.png"),
            size=(image_size, image_size)
        )

        # Add logo with gaming style
        self.splash_label = ctk.CTkLabel(self.splash_content, text="", image=self.logo_image)
        self.splash_label.pack(pady=5)

        # Add a title with gaming font
        self.title_label = ctk.CTkLabel(
            self.splash_content,
            text="GAME CENTER",
            font=("Orbitron", 24, "bold"),
            text_color="#00CCFF"
        )
        self.title_label.pack(pady=(5, 15))

        # Create a progress bar for visual feedback
        self.progress_bar = ctk.CTkProgressBar(
            self.splash_content,
            width=350,
            height=12,
            corner_radius=0,
            progress_color="#00CCFF",
            fg_color="#111111"
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 15))

        # Status text with futuristic font
        self.status_label = ctk.CTkLabel(
            self.splash_content,
            text="INITIALIZING SYSTEM",
            font=("Orbitron", 16),
            text_color="#FFFFFF"
        )
        self.status_label.pack()

        # Version info at the bottom corner
        self.version_label = ctk.CTkLabel(
            self,
            text="v1.1.0",
            font=("Orbitron", 12),
            text_color="#555555"
        )
        self.version_label.place(relx=0.98, rely=0.98, anchor="se")

    def start_animation_and_updates(self):
        # Start the fade-in animation
        self.fade_in()

    def fade_in(self):
        # Start with black screen
        self.master.attributes('-alpha', 0)

        # Fade in effect
        for i in range(0, 101, 2):
            self.master.attributes('-alpha', i/100)
            self.master.update()
            time.sleep(0.01)

        # Start the update process in a separate thread
        self.progress_bar.set(0.2)  # Initial progress
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def check_for_updates(self):
        # Step 1: Check internet
        self.status_label.configure(text="CHECKING CONNECTION")
        self.progress_bar.set(0.3)
        time.sleep(0.5)  # Small delay for visual effect

        have_internet = self.check_internet()
        self.progress_bar.set(0.5)

        # Step 2: Update based on connection
        if have_internet:
            self.status_label.configure(text="UPDATING SYSTEM")
            self.progress_bar.set(0.7)
            self.update_repo()
        else:
            self.status_label.configure(text="OFFLINE MODE")
            self.progress_bar.set(0.9)

        # Final progress
        self.progress_bar.set(1.0)

        # Flash the progress bar to indicate completion
        self.flash_progress_bar()

        # Wait 2 seconds before fading out
        self.after(2000, self.fade_out)

    def flash_progress_bar(self):
        """Add a flashing effect to the progress bar on completion"""
        original_color = self.progress_bar.cget("progress_color")

        def flash_once():
            self.progress_bar.configure(progress_color="#FFFFFF")
            self.after(100, lambda: self.progress_bar.configure(progress_color=original_color))

        flash_once()
        self.after(300, flash_once)  # Flash twice

    def fade_out(self):
        # Fade out with a slight delay
        self.status_label.configure(text="LAUNCHING")

        for i in range(100, -1, -2):
            self.master.attributes('-alpha', i/100)
            self.master.update()
            time.sleep(0.01)

        # Transition to main UI
        self.on_close()

    def check_internet(self, host="8.8.8.8", port=53, timeout=3):
        """Check if there is an active internet connection."""
        try:
            socket.setdefaulttimeout(timeout)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.close()
            self.status_label.configure(text="CONNECTION ESTABLISHED")
            return True
        except socket.error:
            self.status_label.configure(text="OFFLINE MODE")
            print("No internet connection.")
            return False

    def update_repo(self):
        """Pull the latest changes from the GitHub repository and restart if necessary."""
        try:
            repo_path = current_path
            result = subprocess.run(["git", "pull"], cwd=repo_path, capture_output=True, text=True)

            if "Already up to date." in result.stdout:
                self.status_label.configure(text="SYSTEM UP TO DATE")

            elif "Please commit" in result.stderr or "Your local changes" in result.stderr:
                self.status_label.configure(text="RESETTING LOCAL CHANGES")
                # Forcefully discard local changes
                subprocess.run(["git", "reset", "--hard"], cwd=repo_path)
                # Try pulling again
                retry_result = subprocess.run(["git", "pull"], cwd=repo_path, capture_output=True, text=True)

                if "Already up to date." in retry_result.stdout or "Updating" in retry_result.stdout:
                    self.status_label.configure(text="UPDATE COMPLETE - RESTARTING")
                    time.sleep(2)
                    self.master.quit()
                else:
                    self.status_label.configure(text="UPDATE ERROR")
                    print("Git pull failed after reset:", retry_result.stderr)

            elif "Updating" in result.stdout:
                self.status_label.configure(text="UPDATE COMPLETE - RESTARTING")
                time.sleep(2)
                self.master.quit()

            else:
                self.status_label.configure(text="UPDATE ERROR")
                print("Git pull failed:", result.stderr)

        except Exception as e:
            self.status_label.configure(text="UPDATE ERROR")
            print("Exception while updating repository:", str(e))
