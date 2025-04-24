import customtkinter as ctk
from PIL import Image, ImageTk
import os, subprocess
import time
import threading
import socket, pathlib


current_path = pathlib.Path(__file__).parent.resolve()

# listener = subprocess.Popen(["sudo","python3",f"{current_path}/gpio_listener.py"])


class GameApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Center")
        self.attributes('-fullscreen', True)
        self.configure(fg_color="black")
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.transitioning = False
        self.last_select_item = time.time()


        # Initialize variables needed for main UI
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.closing = 0
        self.after(500,self.set_focus)
        
        self.update_idletasks()
        self.set_focus()
               
        self.last_closing_attempt = time.time()

        # Start with splash screen
        self.show_splash_screen()
        
        # Repo path
        self.repo_path = os.path.dirname(os.path.abspath(__file__)) 
    
    def set_focus(self):
        self.focus_force()
        self.attributes('-topmost',True)
        self.attributes('-fullscreen',True)
        self.after(2000, lambda: os.system("xdotool search --name 'Game Center' windowactivate"))
        self.update_idletasks()
        
    def show_splash_screen(self):
        # Create a stylish black frame
        self.splash_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.splash_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Create a center content container
        self.splash_content = ctk.CTkFrame(self.splash_frame, fg_color="#000000")
        self.splash_content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Stylish logo
        image_size = min(self.screen_width, self.screen_height) * 0.4
        self.logo_image = ctk.CTkImage(
            dark_image=Image.open(f"{current_path}/logo.png"),
            size=(image_size, image_size)
        )
        
        # Add logo with gaming style
        self.splash_label = ctk.CTkLabel(self.splash_content, text="", image=self.logo_image)
        self.splash_label.pack(pady=20)
        
        # Add a title with gaming font
        self.title_label = ctk.CTkLabel(
            self.splash_content, 
            text="GAME CENTER", 
            font=("Orbitron", 32, "bold"), 
            text_color="#00CCFF"
        )
        self.title_label.pack(pady=(5, 25))
        
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
            self.splash_frame, 
            text="v1.0.0", 
            font=("Orbitron", 12), 
            text_color="#555555"
        )
        self.version_label.place(relx=0.98, rely=0.98, anchor="se")
        
        # Start the fade-in animation
        self.fade_in()

    def fade_in(self):
        # Start with black screen
        self.attributes('-alpha', 0)
        
        # Fade in effect
        for i in range(0, 101, 2):
            self.attributes('-alpha', i/100)
            self.update()
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
        self.status_label.after(2000, self.fade_out)

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
            self.attributes('-alpha', i/100)
            self.update()
            time.sleep(0.01)
        
        # Transition to main UI
        self.transition_to_main_ui()

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
            result = subprocess.run(["git", "pull"], cwd=self.repo_path, capture_output=True, text=True)
            
            if "Already up to date." in result.stdout:
                self.status_label.configure(text="SYSTEM UP TO DATE")
            else:
                self.status_label.configure(text="UPDATE COMPLETE - RESTARTING")
                time.sleep(2)
                # Close the current application, startup script will run the new version
                self.quit()

        except Exception as e:
            self.status_label.configure(text="UPDATE ERROR")
            print("Error updating repository:", str(e))

    def transition_to_main_ui(self):
        # Clean up splash screen
        self.splash_frame.destroy()
        
        # Initialize main UI
        self.setup_main_ui()
        
        # Fade in main UI
        self.fade_in_main()

    def fade_in_main(self):
        # Fade in main UI
        for i in range(0, 101, 2):
            self.attributes('-alpha', i/100)
            self.update()
            time.sleep(0.01)
    
    def setup_main_ui(self):
        self.title("Game Info App")


        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        # Content Frame
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="#2D2D2D", corner_radius=15)
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        # Footer
        self.footer_label = ctk.CTkLabel(
            self.main_container,
            text="Created with ❤ by Orchids powered by STEM",
            font=("Orbitron", 20, "bold"),
            text_color="#888888"
        )
        self.footer_label.place(relx=0.5, rely=0.98, anchor="center")

        # Scrollable Game List
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="#202020",
            corner_radius=15,
            width=int(self.screen_width * 0.25)
        )
        self.scroll_frame.place(relx=0.02, rely=0.5, anchor="w", relwidth=0.28, relheight=0.95)

        # Game Buttons
        self.items = []
        self.games_dict = {}  # Store game type and path
        
        all_games = []
        game_folder = f"{current_path}/games"
        files = os.listdir(game_folder)
        for file in files:
            if file.endswith(".py") or  file.endswith(".zip"):
                all_games.append(file)

        for file in all_games:
            if file.endswith(".py"):
                name = file.split(".")[0]
                self.games_dict[name] = {"path": f"{game_folder}/{file}", "type": "python"}
            
            elif file.endswith(".zip"):  # Detect zipped ROM files
                name = file.split(".")[0]
                self.games_dict[name] = {"path": f"{game_folder}/{file}", "type": "emulator"}


            # Create buttons for all detected games
            button = GameButton(self.scroll_frame, text=name, height=int(self.screen_height * 0.05))
            button.pack(pady=5, padx=10, fill="x")
            self.items.append(button)

        # Right Content Area
        self.right_content = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.right_content.place(relx=0.35, rely=0.02, relwidth=0.63, relheight=0.95)

        # Image Display
        self.image_frame = ctk.CTkFrame(self.right_content, fg_color="#202020", corner_radius=15)
        self.image_frame.place(relx=0, rely=0, relwidth=1, relheight=0.7)
        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Description Panel
        self.desc_frame = ctk.CTkFrame(self.right_content, fg_color="#202020", corner_radius=15)
        self.desc_frame.place(relx=0, rely=0.75, relwidth=1, relheight=0.25)
        self.desc_label = ctk.CTkLabel(
            self.desc_frame,
            text="",
            wraplength=int(self.screen_width * 0.5),
            font=("Orbitron", 16),
            text_color="#FFFFFF"
        )
        self.desc_label.place(relx=0.5, rely=0.5, anchor="center")

        # Initialize selection
        self.selected_index = 0
        self.update_selection()

        # Input Bindings
        self.bind("<KeyPress-w>", self.move_up)
        self.bind("<KeyPress-s>", self.move_down)
        self.bind("<KeyPress-space>", self.select_item)
        self.bind("<KeyPress-Escape>", self.close_window)
    
    def read_txt(self, game_name):
        try:
            with open(f"{current_path}/games/games_texts/{game_name}.txt", 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "No Description"
        
    def update_selection(self):
        for i, button in enumerate(self.items):
            if i == self.selected_index:
                button.set_selected(True)

                # Load and display game image
                image_path = f"{current_path}/games/games_images/{button.cget('text')}.jpg"
                image_width = int(self.screen_width * 0.5)
                image_height = int(self.screen_height * 0.4)

                threading.Thread(
                    target=self.fade_image,
                    args=(image_path, image_width, image_height),
                    daemon=True
                ).start()

                # Load and display game description
                text = self.read_txt(button.cget('text'))
                self.desc_label.configure(
                    text=f"{button.cget('text')}\n"
                        f"{text}"
                )

                # Calculate scroll position to center the selected item
                button.update_idletasks()
                scroll_frame_height = self.scroll_frame.winfo_height()
                button_height = button.winfo_height()
                button_y = button.winfo_y()
                
                # Calculate the center position of the button
                button_center = button_y + button_height / 2
                
                # Calculate the desired scroll position to center the button
                scroll_fraction = (button_center - scroll_frame_height / 2) / (len(self.items) * button_height)
                
                # Ensure scroll fraction stays within bounds (0-1)
                scroll_fraction = max(0, min(scroll_fraction, 1))
                
                # Apply the scroll
                self.scroll_frame._parent_canvas.yview_moveto(scroll_fraction)
                
            else:
                button.set_selected(False)

    def fade_image(self, new_image_path, target_width, target_height):
        try:
            steps = 10
            overlay = Image.open(new_image_path).convert("RGBA")
            resized_overlay = overlay.resize((target_width, target_height), Image.LANCZOS)

            for alpha in range(0, 255 + int(255 / steps), int(255 / steps)):
                temp_overlay = resized_overlay.copy()
                temp_overlay.putalpha(alpha)

                temp_image = ImageTk.PhotoImage(temp_overlay)
                self.image_label.configure(image=temp_image)
                self.image_label.image = temp_image
                self.update()
                time.sleep(0.02)

            final_image_tk = ImageTk.PhotoImage(resized_overlay)
            self.image_label.configure(image=final_image_tk)
            self.image_label.image = final_image_tk

        except FileNotFoundError:
            self.image_label.configure(image=None, text="Image not found")

    def move_up(self, event):
        if self.selected_index > 0:
            self.selected_index -= 1
            self.update_selection()

    def move_down(self, event):
        if self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            self.update_selection()

    def select_item(self, event):
        if time.time() - self.last_select_item > 0.5:
            selected_item = self.items[self.selected_index]
            game_name = selected_item.cget("text")
            game_info = self.games_dict.get(game_name)

            if game_info:
                game_path = game_info["path"]
                
                if game_info["type"] == "python":
                    os.system(f"python {game_path}")  # Run Pygame game
                    
                elif game_info["type"] == "emulator":
                    
                    os.system(f"/usr/games/mgba-qt {game_path}")  # Run GBA/GB game with mGBA emulator


            self.last_select_item = time.time()

    def close_window(self, event):
        current_time = time.time()
        time_diff = current_time - self.last_closing_attempt
        
        if time_diff >= 1:
            self.closing = 0
            
        self.closing += 1
        if self.closing >= 10:
            self.quit() 
            # listener.terminate()
            # listener.wait()
            
        self.last_closing_attempt = current_time

    def on_close(self):
        self.transitioning = True
        self.quit()

class GameButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.configure(
            corner_radius=12,
            fg_color="#202020",  # Deep matte black
            hover_color="#2D2D2D",  # Softer contrast
            text_color="#EDEDED",  # Softer white
            font=("Orbitron", 17),  # Sleek & modern font
            border_width=2,
            border_color="#333333"
        )

    def set_selected(self, selected):
        if selected:
            self.configure(
                fg_color="#0D6EFD",  # Vibrant blue
                border_color="#0A58CA",
                hover_color="#1A74E9",
                text_color="#FFFFFF"  # Brighter text for contrast
            )
        else:
            self.configure(
                fg_color="#202020",
                border_color="#333333",
                hover_color="#2D2D2D",
                text_color="#EDEDED"
            )


# Run the Application
if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
    
