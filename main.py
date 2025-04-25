import customtkinter as ctk
from PIL import Image, ImageTk
import os, subprocess
import time
import threading
import socket, pathlib
from itertools import cycle


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
        # self.after(500,self.set_focus)
        
        self.update_idletasks()
        # self.set_focus()
               
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
        # Theme colors
        dark_bg = "#121212"
        panel_bg = "#1A1A1A"
        accent_color = "#FF5722"  # Vibrant orange accent
        secondary_accent = "#8C52FF"  # Purple secondary accent
        highlight_color = "#2196F3"  # Blue highlight
        text_primary = "#FFFFFF"
        text_secondary = "#AAAAAA"

        # Main Container with dark gaming background
        self.main_container = ctk.CTkFrame(self, fg_color=dark_bg, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        
        # Header frame - set height in constructor
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color=panel_bg, height=60, corner_radius=0)
        self.header_frame.pack(fill="x", pady=(0, 15))
        
        # Create glossy logo effect
        logo_text = "ORCHIDS GAME HUB"
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text=logo_text,
            font=("Orbitron", 28, "bold"),
            text_color=accent_color
        )
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        

        # Content Frame - Main area with rounded corners
        self.content_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color=panel_bg, 
            corner_radius=20,
            border_width=2,
            border_color=accent_color
        )
        self.content_frame.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.95, relheight=0.82)
        


        # Scrollable Game List with title
        self.games_title = ctk.CTkLabel(
            self.content_frame,
            text="GAME LIBRARY",
            font=("Orbitron", 16, "bold"),
            text_color=accent_color
        )
        self.games_title.place(relx=0.02, rely=0.04)
        

        # Improved scrollable game list
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="#151515",
            corner_radius=15,
            width=int(self.screen_width * 0.25),
            border_width=1,
            border_color="#333333"
        )
        self.scroll_frame.place(relx=0.02, rely=0.52, anchor="w", relwidth=0.28, relheight=0.83)

        # Game Buttons
        self.items = []
        self.games_dict = {}  # Store game type and path
        
        all_games = []
        game_folder = f"{current_path}/games"
        files = os.listdir(game_folder)
        for file in files:
            if file.endswith(".py") or file.endswith(".zip"):
                all_games.append(file)

        for file in all_games:
            if file.endswith(".py"):
                name = file.split(".")[0]
                self.games_dict[name] = {"path": f"{game_folder}/{file}", "type": "python"}
            
            elif file.endswith(".zip"):  # Detect zipped ROM files
                name = file.split(".")[0]
                self.games_dict[name] = {"path": f"{game_folder}/{file}", "type": "emulator"}

            # Create buttons for all detected games with enhanced styling
            button = GameButton(
                self.scroll_frame, 
                text=name, 
                height=int(self.screen_height * 0.07),
                fg_color="#252525",
                hover_color="#303030",
                corner_radius=10
            )
            button.pack(pady=5, padx=8, fill="x")
            self.items.append(button)

        # Right Content Area - Game details
        self.right_content = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.right_content.place(relx=0.33, rely=0.02, relwidth=0.65, relheight=0.96)

        # Game image display with glow effect border
        self.image_frame = ctk.CTkFrame(
            self.right_content, 
            fg_color="#151515", 
            corner_radius=15,
            border_width=2,
            border_color=secondary_accent
        )
        self.image_frame.place(relx=0, rely=0, relwidth=1, relheight=0.65)
        
        # Game title overlay on image
        self.game_title_frame = ctk.CTkFrame(
            self.image_frame,
            fg_color="#161616",  # Dark color instead of semi-transparent 
            corner_radius=10,
            height=40
        )
        self.game_title_frame.place(relx=0.02, rely=0.02, relwidth=0.4)
        
        self.game_title = ctk.CTkLabel(
            self.game_title_frame,
            text="SELECT A GAME",
            font=("Orbitron", 16, "bold"),
            text_color=accent_color
        )
        self.game_title.place(relx=0.5, rely=0.5, anchor="center")
        
        # Image display area
        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Game controls overlay
        self.controls_frame = ctk.CTkFrame(
            self.image_frame,
            fg_color="#161616",  # Dark color instead of semi-transparent
            corner_radius=10,
            height=40
        )
        self.controls_frame.place(relx=0.98, rely=0.98, relwidth=0.3, anchor="se")
        
        
        self.controls_label = ctk.CTkLabel(
            self.controls_frame,
            text="↑/↓: Navigate | LEFT-TOP: Select",
            font=("Orbitron", 12),
            text_color=text_secondary
        )
        self.controls_label.place(relx=0.5, rely=0.5, anchor="center")

        # Game info panel with tabs
        self.info_frame = ctk.CTkTabview(
            self.right_content,
            fg_color="#151515",
            corner_radius=15,
            border_width=1,
            border_color="#333333",
            segmented_button_fg_color="#252525",
            segmented_button_selected_color=accent_color,
            segmented_button_selected_hover_color=highlight_color,
            text_color=text_primary
        )
        self.info_frame.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
        
        # Create tabs
        self.info_frame.add("DESCRIPTION")
        
        # Description tab content
        self.desc_label = ctk.CTkLabel(
            self.info_frame.tab("DESCRIPTION"),
            text="Select a game to view its description",
            wraplength=int(self.screen_width * 0.5),
            font=("Orbitron", 14),
            text_color=text_primary,
            justify="left"
        )
        self.desc_label.place(relx=0.02, rely=0.02, relwidth=0.96)
        
    
        # Footer with animated color effect
        self.footer_frame = ctk.CTkFrame(self.main_container, fg_color=panel_bg, height=30, corner_radius=0)
        self.footer_frame.place(relx=0, rely=1, relwidth=1, anchor="sw")
        
        
        self.footer_label = ctk.CTkLabel(
            self.footer_frame,
            text="Created with ❤ by Orchids powered by STEM",
            font=("Orbitron", 14, "bold"),
            text_color="#888888"
        )
        self.footer_label.place(relx=0.5, rely=0.5, anchor="center")

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
                game_name = button.cget('text')
                
                # Update game title
                self.game_title.configure(text=game_name.upper())
                
                # Load and display game image with enhanced fade effect
                image_path = f"{current_path}/games/games_images/{game_name}.jpg"
                image_width = int(self.screen_width * 0.6)
                image_height = int(self.screen_height * 0.4)

                threading.Thread(
                    target=self.fade_image,
                    args=(image_path, image_width, image_height),
                    daemon=True
                ).start()

                # Load and display game description
                text = self.read_txt(game_name)
                self.desc_label.configure(
                    text=text,
                    justify="left"
                )
                

                # Calculate scroll position to center the selected item with animation
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
                
                # Apply the scroll with smooth animation
                current_scroll = self.scroll_frame._parent_canvas.yview()[0]
                self.animate_scroll(current_scroll, scroll_fraction)
                
            else:
                button.set_selected(False)

    def animate_scroll(self, start, end):
        """Smooth scrolling animation"""
        steps = 10
        step_size = (end - start) / steps
        
        def step(current_step):
            if current_step < steps:
                new_pos = start + (step_size * current_step)
                self.scroll_frame._parent_canvas.yview_moveto(new_pos)
                self.after(10, lambda: step(current_step + 1))
            else:
                self.scroll_frame._parent_canvas.yview_moveto(end)
        
        step(1)

    def fade_image(self, new_image_path, target_width, target_height):
        try:
            steps = 5  # More steps for smoother transition
            
            # First fade out current image if exists
            if hasattr(self.image_label, 'image') and self.image_label.image:
                for alpha in range(255, 0, -int(255 / steps)):
                    # Apply alpha to current image
                    if hasattr(self, '_current_image_pil'):
                        temp_overlay = self._current_image_pil.copy()
                        temp_overlay.putalpha(alpha)
                        temp_image = ImageTk.PhotoImage(temp_overlay)
                        self.image_label.configure(image=temp_image)
                        self.image_label.image = temp_image
                        self.update()
                        time.sleep(0.015)
            
            # Now fade in new image with slight pause
            time.sleep(0.05)
            
            overlay = Image.open(new_image_path).convert("RGBA")
            resized_overlay = overlay.resize((target_width, target_height), Image.LANCZOS)
            self._current_image_pil = resized_overlay.copy()  # Store for later fade-out
            
            # Add subtle drop shadow and rounded corners effect
            # (This would be approximated in PIL but actual effects would need more complex image processing)
            
            for alpha in range(0, 255 + int(255 / steps), int(255 / steps)):
                temp_overlay = resized_overlay.copy()
                temp_overlay.putalpha(alpha)

                temp_image = ImageTk.PhotoImage(temp_overlay)
                self.image_label.configure(image=temp_image)
                self.image_label.image = temp_image
                self.update()
                time.sleep(0.015)

            final_image_tk = ImageTk.PhotoImage(resized_overlay)
            self.image_label.configure(image=final_image_tk)
            self.image_label.image = final_image_tk

        except FileNotFoundError:
            # Create a stylish "no image" placeholder
            self.image_label.configure(image=None)
            no_image_frame = ctk.CTkFrame(
                self.image_label, 
                fg_color="#222222", 
                corner_radius=15,
                width=target_width,
                height=target_height
            )
            no_image_frame.place(relx=0.5, rely=0.5, anchor="center")
            
            no_image_label = ctk.CTkLabel(
                no_image_frame,
                text="No Image Available",
                font=("Orbitron", 24, "bold"),
                text_color="#555555"
            )
            no_image_label.place(relx=0.5, rely=0.5, anchor="center")

    def move_up(self, event):
        if self.selected_index > 0:
            self.selected_index -= 1
            self.update_selection()

    def move_down(self, event):
        if self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            self.update_selection()
    
    def select_item(self, event=None):
        # Prevent rapid clicking/selection
            
        if time.time() - self.last_select_item > 0.5:
            # Visual feedback when game is selected
            selected_button = self.items[self.selected_index]
            selected_button.configure(fg_color="#FF5722")  # Highlight with accent color
            
            # Get game information
            game_name = selected_button.cget("text")
            game_info = self.games_dict.get(game_name)
            
            self.update()
            
            if game_info:
                game_path = game_info["path"]
                launch_success = False
                
                try:
                    # Create launch command based on game type
                    if game_info["type"] == "python":
                        # Run Pygame game
                        subprocess.Popen(["python", game_path], 
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                        launch_success = True
                        
                    elif game_info["type"] == "emulator":
                        # Run GBA/GB game with mGBA emulator
                        subprocess.Popen(["/usr/games/mgba-qt", game_path],
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                        launch_success = True
                        
                    # Handle launch result
                    if launch_success:
                        pass
                    else:
                        # Show error if launch failed
                        self.show_notification(f"Failed to launch {game_name}", "error")
                        
                except Exception as e:
                    # Handle any exceptions during launch
                    error_msg = str(e)
                    self.show_notification(f"Error launching {game_name}: {error_msg}", "error")
                    
            # Reset button appearance after short delay
            self.after(300, lambda: selected_button.configure(fg_color="#252525"))
            
            # Update timestamp to prevent rapid clicking
            self.last_select_item = time.time()

    def show_notification(self, message, notification_type="info"):
        """Show a temporary notification message"""
        colors = {
            "info": "#2196F3",  # Blue
            "success": "#4CAF50",  # Green
            "error": "#F44336"  # Red
        }
        
        # Create notification frame
        if hasattr(self, 'notification_frame'):
            self.notification_frame.destroy()
            
        self.notification_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=colors.get(notification_type, "#2196F3"),
            corner_radius=10,
            height=40
        )
        self.notification_frame.place(relx=0.5, rely=0.95, anchor="center", relwidth=0.3)
        
        # Notification text
        notification_label = ctk.CTkLabel(
            self.notification_frame,
            text=message,
            font=("Orbitron", 14, "bold"),
            text_color="#FFFFFF"
        )
        notification_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Auto-hide after 3 seconds
        self.after(3000, lambda: self.notification_frame.destroy() if hasattr(self, 'notification_frame') else None)

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
    
