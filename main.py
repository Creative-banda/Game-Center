import customtkinter as ctk
from PIL import Image, ImageTk
import os, subprocess
import time
import threading
import socket, pathlib


current_path = pathlib.Path(__file__).parent.resolve()

listener = subprocess.Popen(["sudo","python3",f"{current_path}/gpio_listener.py"])


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
        self.splash_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.splash_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        image_size = min(self.screen_width, self.screen_height) * 0.5
        self.logo_image = ctk.CTkImage(
            dark_image=Image.open(f"{current_path}/logo.png"),
            size=(image_size, image_size)
        )
        
        self.splash_label = ctk.CTkLabel(self.splash_frame, text="", image=self.logo_image)
        self.splash_label.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(
            self.splash_frame, text="Checking for updates...", font=("Roboto", 18), text_color="white"
        )
        self.status_label.pack()
        
        self.fade_in()
        
    def fade_in(self):
        for i in range(0, 101, 2):
            self.attributes('-alpha', i/100)
            self.update()
            time.sleep(0.01)
        
        threading.Thread(target=self.check_for_updates, daemon=True).start()
    
    def check_for_updates(self):
        self.status_label.configure(text="Checking internet connection...")
        have_internet = self.check_internet()
        
        if have_internet:
            self.status_label.configure(text="Updating console...")
            self.update_repo()
        else:
            self.status_label.configure(text="No internet connection.")
        
        time.sleep(2)
        
        self.fade_out()
    
    def fade_out(self):
        for i in range(100, -1, -2):
            self.attributes('-alpha', i/100)
            self.update()
            time.sleep(0.01)
        self.transition_to_main_ui()
        
    def check_internet(self, host="8.8.8.8", port=53, timeout=3):
        """Check if there is an active internet connection."""
        try:
            socket.setdefaulttimeout(timeout)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.close()  # Properly close the socket
            self.status_label.configure(text="Connected to the internet.")
            return True
        except socket.error:
            print("No internet connection.")
            return False        

    def update_repo(self):
        """Pull the latest changes from the GitHub repository and restart if necessary."""
        try:
            result = subprocess.run(["git", "pull"], cwd=self.repo_path, capture_output=True, text=True)
            
            self.status_label.configure(text="Checking for updates...")

            if "Already up to date." in result.stdout:
                self.status_label.configure(text="No updates available.")
            else:
                self.status_label.configure(text="Update successful. Restarting...")
                time.sleep(2)
                # Close the current application, startup script will run the new version
                self.quit()  


        except Exception as e:
            print("Error updating repository:", str(e))

    def transition_to_main_ui(self):
        self.splash_frame.destroy()
        self.setup_main_ui()
        self.fade_in_main()
    
    def fade_in_main(self):
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
            font=("Roboto", 16),
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

                image_path = f"{current_path}/games/games_images/{button.cget('text')}.jpg"
                image_width = int(self.screen_width * 0.5)
                image_height = int(self.screen_height * 0.4)

                threading.Thread(
                    target=self.fade_image,
                    args=(image_path, image_width, image_height),
                    daemon=True
                ).start()
                text = self.read_txt(button.cget('text'))
                self.desc_label.configure(
                    text=f"{button.cget('text')}\n"
                         f"{text}"
                )

                button.update_idletasks()
                button_y = button.winfo_y()
                scroll_frame_height = self.scroll_frame.winfo_height()
                button_height = button.winfo_height()

                total_content_height = len(self.items) * button_height
                visible_fraction = scroll_frame_height / total_content_height
                scroll_fraction = button_y / (total_content_height - scroll_frame_height)

                scroll_fraction = max(0, min(scroll_fraction, 1 - visible_fraction))
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
            listener.terminate()
            listener.wait()
            
        self.last_closing_attempt = current_time

    def on_close(self):
        self.transitioning = True
        self.quit()

class GameButton(ctk.CTkButton):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.configure(
            corner_radius=10,
            fg_color="#2B2B2B",
            hover_color="#3B3B3B",
            text_color="#FFFFFF",
            font=("Roboto", 16),
            border_width=2,
            border_color="#1A1A1A"
        )

    def set_selected(self, selected):
        if selected:
            self.configure(
                fg_color="#1A84D6",
                border_color="#0A5AAD",
                hover_color="#1976C2"
            )
        else:
            self.configure(
                fg_color="#2B2B2B",
                border_color="#1A1A1A",
                hover_color="#3B3B3B"
            )

# Run the Application
if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
    
