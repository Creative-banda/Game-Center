import customtkinter as ctk
from PIL import Image, ImageTk
import os, subprocess
import time
import threading
import socket

from pathlib import Path


current_path = Path(__file__).parent.resolve()

screenshots_folder = current_path / 'screenshots'

# Make sure the screenshots folder exists (create it once at the start)
screenshots_folder.mkdir(exist_ok=True)


listener = subprocess.Popen(["sudo","python3",f"{current_path}/gpio_listener.py"])


class GameApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Center")
        self.attributes('-fullscreen', True)
        self.configure(fg_color="black")
        self.configure(cursor="none")  # Hide mouse cursor
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.transitioning = False
        self.last_select_item = time.time()


        # Initialize variables needed for main UI
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.closing = 0
        self.after(500,self.set_focus)
        
        
        self.games_selected_index = 0
        self.screenshot_selected_index = 0
        
        self.update_idletasks()
        self.set_focus()
               
        self.last_closing_attempt = time.time()

        # Start with splash screen
        self.show_splash_screen()
        
        # Repo path
        self.repo_path = os.path.dirname(os.path.abspath(__file__)) 
        
        # Last ScreenShot Time
        
        self.last_screenshot = time.time()  # Fixed the assignment to use time.time() correctly
    
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
        image_size = min(self.screen_width, self.screen_height) * 0.7
        self.logo_image = ctk.CTkImage(
            dark_image=Image.open(f"{current_path}/logo.png"),
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
            self.splash_frame, 
            text="v1.1.0", 
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
            font=("Orbitron", 24, "bold"),
            text_color=accent_color
        )
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Content Frame
        self.content_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color=panel_bg, 
            corner_radius=20,
            border_width=2,
            border_color=accent_color
        )
        self.content_frame.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.95, relheight=0.82)
        
        # Tab system for Games and Screenshots
        self.tab_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tab_frame.place(relx=0.02, rely=0.01, relwidth=0.28)
        
        # Create tab buttons
        self.tab_buttons = []
        self.tabs = ["GAMES", "SCREENSHOTS"]
        self.current_tab = "GAMES"  # Default tab
        
        for i, tab_name in enumerate(self.tabs):
            tab_button = ctk.CTkButton(
                self.tab_frame,
                text=tab_name,
                font=("Orbitron", 10, "bold"),
                fg_color="#252525" if tab_name != self.current_tab else accent_color,
                hover_color="#303030" if tab_name != self.current_tab else highlight_color,
                text_color=text_primary,
                corner_radius=10,
                height=35,
                width=int(self.screen_width * 0.12),
                command=lambda t=tab_name: self.switch_tab(t)
            )
            tab_button.place(relx=0.5*i, rely=0, anchor="nw")
            self.tab_buttons.append(tab_button)
            
        # Games title below tabs
        self.games_title = ctk.CTkLabel(
            self.content_frame,
            text="GAME LIBRARY",
            font=("Orbitron", 13, "bold"),
            text_color=accent_color
        )
        self.games_title.place(relx=0.02, rely=0.1)
        

        self.scroll_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="#151515",
            corner_radius=15,
            width=int(self.screen_width * 0.25),
            border_width=1,
            border_color="#333333",
            scrollbar_button_color="#151515",  # Match scrollbar color to background
            scrollbar_button_hover_color="#151515"  # Match hover color to background
        )
        self.scroll_frame.place(relx=0.02, rely=0.58, anchor="w", relwidth=0.28, relheight=0.75)

        # Game Buttons
        self.items = []
        self.games_dict = {}  # Store game type and path
        
        # Screenshots frame (initially hidden)
        self.screenshot_scroll_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="#151515",
            corner_radius=15,
            width=int(self.screen_width * 0.25),
            border_width=1,
            border_color="#333333",
            scrollbar_button_color="#151515",  # Match scrollbar color to background
            scrollbar_button_hover_color="#151515"  # Match hover color to background
        )
        self.screenshot_scroll_frame.place(relx=0.02, rely=0.58, anchor="w", relwidth=0.28, relheight=0.75)
        self.screenshot_scroll_frame.place_forget()  # Initially hidden

        # Screenshots Items
        self.screenshot_items = []
        self.screenshot_paths = []
        
        # Load games
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
        
        # Load screenshots
        self.load_screenshots()

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
        self.image_label.place(relx=0.5, rely=0.55, anchor="center")


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
            font=("Orbitron", 10),
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
        self.bind("<KeyPress-a>", self.previous_tab)
        self.bind("<KeyPress-d>", self.next_tab)
        self.bind("<KeyPress-space>", self.select_item)
        self.bind("<KeyPress-f>", self.delete_screenshot)
        self.bind("<KeyPress-Escape>", self.close_window)

    def select_screenshot(self, index):
        self.screenshot_selected_index = index
        self.update_selection()


    def load_screenshots(self):
        print("Loading screenshots...")
        """Load screenshots from the screenshots folder"""
        self.screenshot_items = []
        self.screenshot_paths = []

        screenshot_folder = f"{current_path}/screenshots"
        
        # Create folder if it doesn't exist
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
            
        # Get all image files
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        files = os.listdir(screenshot_folder)
        screenshot_files = [f for f in files if os.path.splitext(f)[1].lower() in valid_extensions]
        
        # Clear existing items
        for widget in self.screenshot_scroll_frame.winfo_children():
            widget.destroy()

        # Create thumbnail buttons for screenshots
        for file in screenshot_files:
            screenshot_path = f"{screenshot_folder}/{file}"
            self.screenshot_paths.append(screenshot_path)

            try:
                pil_img = Image.open(screenshot_path)
                pil_img.thumbnail((int(self.screen_width * 0.06), int(self.screen_height * 0.05)))
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img,
                                    size=(int(self.screen_width * 0.06), int(self.screen_height * 0.05)))
            except Exception as e:
                ctk_img = None  # If image loading fails

            # Create button directly
            btn = ctk.CTkButton(
                self.screenshot_scroll_frame,
                text=file[:15] + "..." if len(file) > 15 else file,
                image=ctk_img,
                anchor="w",
                compound="left",
                height=int(self.screen_height * 0.07),
                fg_color="#252525",
                hover_color="#353535",
                font=("Orbitron", 12),
                command=lambda path=screenshot_path, idx=len(self.screenshot_items): self.select_screenshot(idx)
            )
            btn.pack(pady=5, padx=8, fill="x")

            self.screenshot_items.append(btn)



    def switch_tab(self, tab_name):
        """Switch between Games and Screenshots tabs"""
        self.current_tab = tab_name
        
        # Update tab button colors
        accent_color = "#FF5722"  # Vibrant orange accent
        highlight_color = "#2196F3"  # Blue highlight
        
        for i, name in enumerate(self.tabs):
            self.tab_buttons[i].configure(
                fg_color="#252525" if name != tab_name else accent_color,
                hover_color="#303030" if name != tab_name else highlight_color
            )
        
        # Hide/show appropriate frames
        if tab_name == "GAMES":
            self.scroll_frame.place(relx=0.02, rely=0.52, anchor="w", relwidth=0.28, relheight=0.75)
            self.screenshot_scroll_frame.place_forget()
            self.games_title.configure(text="GAME LIBRARY")
        else:  # SCREENSHOTS
            self.load_screenshots()
            self.scroll_frame.place_forget()
            self.screenshot_scroll_frame.place(relx=0.02, rely=0.52, anchor="w", relwidth=0.28, relheight=0.75)
            self.games_title.configure(text="SCREENSHOTS")
        
        # Update selection highlighting
        self.update_selection()

    def previous_tab(self, event=None):
        """Switch to the previous tab using A key"""
        current_index = self.tabs.index(self.current_tab)
        new_index = (current_index - 1) % len(self.tabs)
        self.switch_tab(self.tabs[new_index])

    def next_tab(self, event=None):
        """Switch to the next tab using D key"""
        current_index = self.tabs.index(self.current_tab)
        new_index = (current_index + 1) % len(self.tabs)
        self.switch_tab(self.tabs[new_index])

    def delete_screenshot(self, event=None):
        """Handle screenshot deletion with confirmation dialog"""
        if self.current_tab != "SCREENSHOTS" or not self.screenshot_paths or self.screenshot_selected_index >= len(self.screenshot_paths):
            return
            
        # Get the path of the selected screenshot
        screenshot_path = self.screenshot_paths[self.screenshot_selected_index]
        file_name = os.path.basename(screenshot_path)
        
        # Create confirmation dialog
        self.confirm_dialog = ctk.CTkToplevel(self)
        self.confirm_dialog.title("Confirm Deletion")
        self.confirm_dialog.geometry("400x150")
        self.confirm_dialog.resizable(False, False)
        self.confirm_dialog.configure(fg_color="#1A1A1A")
        
        # Add a transient attribute (makes dialog a child of the main window)
        self.confirm_dialog.transient(self)
        self.confirm_dialog.grab_set()  # Make dialog modal
        
        # Center the dialog relative to the main window
        x = self.winfo_x() + (self.winfo_width() // 2) - (400 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (150 // 2)
        self.confirm_dialog.geometry(f"+{x}+{y}")
        
        # Dialog content
        message_label = ctk.CTkLabel(
            self.confirm_dialog,
            text=f"Are you sure you want to delete:\n{file_name}?",
            font=("Orbitron", 14),
            text_color="#FFFFFF"
        )
        message_label.pack(pady=20)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.confirm_dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        # Store the current button selection
        self.dialog_selection = 0  # 0 for No, 1 for Yes
        
        # Button styles
        button_width = 100
        button_height = 35
        
        # No button (default)
        self.no_button = ctk.CTkButton(
            button_frame,
            text="No",
            font=("Orbitron", 12, "bold"),
            fg_color="#FF5722",  # Accent color for selected option
            hover_color="#FF7043",
            corner_radius=10,
            width=button_width,
            height=button_height,
            command=lambda: self.confirm_dialog.destroy()
        )
        self.no_button.pack(side="left", padx=10)
        
        # Yes button
        self.yes_button = ctk.CTkButton(
            button_frame,
            text="Yes",
            font=("Orbitron", 12, "bold"),
            fg_color="#252525",  # Default color for unselected option
            hover_color="#303030",
            corner_radius=10,
            width=button_width,
            height=button_height,
            command=lambda: self.delete_confirmed(screenshot_path)
        )
        self.yes_button.pack(side="left", padx=10)
        
        # Bind A/D keys for dialog navigation
        self.confirm_dialog.bind("<KeyPress-a>", self.dialog_previous)
        self.confirm_dialog.bind("<KeyPress-d>", self.dialog_next)
        self.confirm_dialog.bind("<KeyPress-space>", self.dialog_select)
        self.confirm_dialog.bind("<KeyPress-Escape>", lambda e: self.confirm_dialog.destroy())
        
        # Update dialog button selection
        self.update_dialog_selection()

    def update_dialog_selection(self):
        """Update the selection highlighting in the confirmation dialog"""
        if hasattr(self, 'confirm_dialog') and self.confirm_dialog.winfo_exists():
            if self.dialog_selection == 0:  # No selected
                self.no_button.configure(fg_color="#FF5722")
                self.yes_button.configure(fg_color="#252525")
            else:  # Yes selected
                self.no_button.configure(fg_color="#252525")
                self.yes_button.configure(fg_color="#FF5722")

    def dialog_previous(self, event=None):
        """Move dialog selection left (No)"""
        self.dialog_selection = 0
        self.update_dialog_selection()

    def dialog_next(self, event=None):
        """Move dialog selection right (Yes)"""
        self.dialog_selection = 1
        self.update_dialog_selection()

    def dialog_select(self, event=None):
        """Confirm the dialog selection with space key"""
        if hasattr(self, 'confirm_dialog') and self.confirm_dialog.winfo_exists():
            if self.dialog_selection == 0:  # No
                self.confirm_dialog.destroy()
            else:  # Yes
                screenshot_path = self.screenshot_paths[self.screenshot_selected_index]
                self.delete_confirmed(screenshot_path)

    def delete_confirmed(self, path):
        """Delete the screenshot after confirmation"""
        try:
            # Delete the file
            os.remove(path)
            
            # Close the dialog
            if hasattr(self, 'confirm_dialog') and self.confirm_dialog.winfo_exists():
                self.confirm_dialog.destroy()
                
            # Reload screenshots
            self.load_screenshots()
            
            # Reset selected index if needed
            if not self.screenshot_items:
                self.screenshot_selected_index = 0
            elif self.screenshot_selected_index >= len(self.screenshot_items):
                self.screenshot_selected_index = len(self.screenshot_items) - 1
                
            # Update UI
            self.update_selection()
            
        except Exception as e:
            # Show error message
            if hasattr(self, 'confirm_dialog') and self.confirm_dialog.winfo_exists():
                error_label = ctk.CTkLabel(
                    self.confirm_dialog,
                    text=f"Error: {str(e)}",
                    font=("Orbitron", 12),
                    text_color="#FF0000"
                )
                error_label.pack(pady=10)

    def display_screenshot(self, path):

        """Display selected screenshot in the main image area"""
        try:
            # Update title
            file_name = os.path.basename(path)
            self.game_title.configure(text=file_name[:25] + "..." if len(file_name) > 25 else file_name)
            
            # Load and resize image to fit display area
            pil_img = Image.open(path)
            # Calculate aspect ratio preserving size
            img_width, img_height = pil_img.size
            display_width = int(self.screen_width * 0.6)
            display_height = int(self.screen_height * 0.4)
            
            # Calculate scaling factor to fit within display area while maintaining aspect ratio
            width_ratio = display_width / img_width
            height_ratio = display_height / img_height
            scale_factor = min(width_ratio, height_ratio)
            
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            
            # Create CTkImage
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(new_width, new_height))
            self.image_label.configure(image=ctk_img)
            
            # Update description
            file_size = os.path.getsize(path) / 1024  # KB
            file_date = time.ctime(os.path.getmtime(path))
            resolution = f"{img_width}x{img_height}"
            
            desc_text = f"File: {file_name}\nResolution: {resolution}\nSize: {file_size:.1f} KB\nDate: {file_date}"
            self.desc_label.configure(text=desc_text)
            
        except Exception as e:
            self.image_label.configure(image=None, text=f"Error loading image: {str(e)}")
            self.desc_label.configure(text=f"Error: {str(e)}")

    def read_txt(self, game_name):
        try:
            with open(f"{current_path}/games/games_texts/{game_name}.txt", 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "No Description"
        
    def update_selection(self):
        if self.current_tab == "GAMES":
            # Handle game selection
            for i, button in enumerate(self.items):
                if i == self.games_selected_index:
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

                    button_center = button_y + button_height / 2
                    scroll_fraction = (button_center - scroll_frame_height / 2) / (len(self.items) * button_height)
                    scroll_fraction = max(0, min(scroll_fraction, 1))

                    current_scroll = self.scroll_frame._parent_canvas.yview()[0]
                    self.animate_scroll(current_scroll, scroll_fraction, self.scroll_frame)
                else:
                    button.set_selected(False)

        else:
            # Handle screenshot selection
            for i, button in enumerate(self.screenshot_items):  
                if i == self.screenshot_selected_index:
                    button.configure(fg_color="#0D6EFD",  # Vibrant blue
                    border_color="#0A58CA",
                    hover_color="#1A74E9",
                    text_color="#FFFFFF")  # Brighter text for contrast)  # <-- no border
                    # Display selected screenshot
                    if self.screenshot_paths and self.screenshot_selected_index < len(self.screenshot_paths):
                        screenshot_path = self.screenshot_paths[self.screenshot_selected_index]
                        self.display_screenshot(screenshot_path)

                    # Center the selected item in the scroll view
                    button.update_idletasks()
                    scroll_frame_height = self.screenshot_scroll_frame.winfo_height()
                    button_height = button.winfo_height()
                    button_y = button.winfo_y()

                    button_center = button_y + button_height / 2
                    scroll_fraction = (button_center - scroll_frame_height / 2) / (len(self.screenshot_items) * button_height)
                    scroll_fraction = max(0, min(scroll_fraction, 1))
                    current_scroll = self.screenshot_scroll_frame._parent_canvas.yview()[0]
                    self.animate_scroll(current_scroll, scroll_fraction, self.screenshot_scroll_frame)
                else:
                    button.configure(fg_color="#252525", hover_color="#353535")  # unselected


    def animate_scroll(self, start, end, frame=None):
        """Smooth scrolling animation"""
        steps = 10
        step_size = (end - start) / steps
        
        def step(current_step):
            if current_step < steps:
                new_pos = start + (step_size * current_step)
                if frame is None:
                    self.scroll_frame._parent_canvas.yview_moveto(new_pos)
                else:
                    frame._parent_canvas.yview_moveto(new_pos)
                self.after(10, lambda: step(current_step + 1))
            else:
                if frame is None:
                    self.scroll_frame._parent_canvas.yview_moveto(end)
                else:
                    frame._parent_canvas.yview_moveto(end)
        
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
        if self.current_tab == "GAMES":
            if self.games_selected_index > 0:
                self.games_selected_index -= 1
                self.update_selection()
        else:  # Screenshots tab
            if self.screenshot_selected_index > 0:
                self.screenshot_selected_index -= 1
                self.update_selection()

    def move_down(self, event):
        if self.current_tab == "GAMES":
            if self.games_selected_index < len(self.items) - 1:
                self.games_selected_index += 1
                self.update_selection()
        else:  # Screenshots tab
            if self.screenshot_selected_index < len(self.screenshot_items) - 1:
                self.screenshot_selected_index += 1
                self.update_selection()
    
    def select_item(self, event=None):
        """Handle selection based on current tab"""
        if self.current_tab == "GAMES":
            # Original game selection code
            if self.items and self.games_selected_index < len(self.items):
                game_name = self.items[self.games_selected_index].cget("text")
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
                                        
                # Update timestamp to prevent rapid clicking
                self.last_select_item = time.time()

        else:  # SCREENSHOTS
            # For screenshots, just display the full image
            if self.screenshot_paths and self.screenshot_selected_index < len(self.screenshot_paths):
                self.display_screenshot(self.screenshot_paths[self.screenshot_selected_index])

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
            listener.terminate()
            listener.wait()
            
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
            font=("Orbitron", 12),  # Sleek & modern font
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
    
