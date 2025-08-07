import customtkinter as ctk
from PIL import Image, ImageTk
import os, subprocess
import time
import threading
import socket
import pygame

from utils.env_utils import current_path
from widgets import GameButton, AnimatedBackground
from splash import SplashScreen

class MainUI(ctk.CTkFrame):
    def __init__(self, master, sounds):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.sounds = sounds
        self.pack(fill="both", expand=True)

        # Theme colors
        dark_bg = "#121212"
        panel_bg = "#1A1A1A"
        accent_color = "#FF5722"  # Vibrant orange accent
        secondary_accent = "#FF8A65"  # Lighter orange
        highlight_color = "#FFA726"  # Brighter orange
        text_primary = "#FFFFFF"

        # Main Container with dark gaming background
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        
        # Header frame - set height in constructor
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color=panel_bg, height=60, corner_radius=0)
        self.header_frame.pack(fill="x", pady=(10, 20))
        
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
        self.content_frame.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.9, relheight=0.8)
        
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
                width=int(self.master.winfo_screenwidth() * 0.12),
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
            width=int(self.master.winfo_screenwidth() * 0.25),
            border_width=1,
            border_color="#333333",
            scrollbar_button_color="#151515",
            scrollbar_button_hover_color="#151515"
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
            width=int(self.master.winfo_screenwidth() * 0.25),
            border_width=1,
            border_color="#333333",
            scrollbar_button_color="#151515",
            scrollbar_button_hover_color="#151515"
        )
        self.screenshot_scroll_frame.place(relx=0.02, rely=0.58, anchor="w", relwidth=0.28, relheight=0.75)
        self.screenshot_scroll_frame.place_forget()

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
            
            elif file.endswith(".zip"):
                name = file.split(".")[0]
                self.games_dict[name] = {"path": f"{game_folder}/{file}", "type": "emulator"}

            button = GameButton(
                self.scroll_frame, 
                text=name, 
                height=int(self.master.winfo_screenheight() * 0.07),
                fg_color="#252525",
                hover_color="#303030",
                corner_radius=10
            )
            button.pack(pady=8, padx=10, fill="x")
            self.items.append(button)
        
        # Load screenshots
        self.load_screenshots()

        # Right Content Area - Game details
        self.right_content = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.right_content.place(relx=1.0, rely=0.02, relwidth=0.65, relheight=0.96)

        self.image_frame = ctk.CTkFrame(
            self.right_content, 
            fg_color="#151515", 
            corner_radius=15,
            border_width=2,
            border_color=secondary_accent
        )
        self.image_frame.place(relx=0, rely=0, relwidth=1, relheight=0.65)
        
        self.game_title_frame = ctk.CTkFrame(
            self.image_frame,
            fg_color="#161616",
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
        
        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        self.image_label.place(relx=0.5, rely=0.55, anchor="center")

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
        
        self.info_frame.add("DESCRIPTION")
        
        self.desc_label = ctk.CTkLabel(
            self.info_frame.tab("DESCRIPTION"),
            text="Select a game to view its description",
            wraplength=int(self.master.winfo_screenwidth() * 0.5),
            font=("Orbitron", 10),
            text_color=text_primary,
            justify="left"
        )
        self.desc_label.place(relx=0.02, rely=0.02, relwidth=0.96)
        
        self.footer_frame = ctk.CTkFrame(self.main_container, fg_color=panel_bg, height=30, corner_radius=0)
        self.footer_frame.place(relx=0, rely=1, relwidth=1, anchor="sw")
        
        self.footer_label = ctk.CTkLabel(
            self.footer_frame,
            text="Created with ❤ by Orchids powered by STEM",
            font=("Orbitron", 14, "bold"),
            text_color="#888888"
        )
        self.footer_label.place(relx=0.5, rely=0.5, anchor="center")

        self.games_selected_index = 0
        self.screenshot_selected_index = 0
        self.update_selection()

    def select_screenshot(self, index):
        self.screenshot_selected_index = index
        self.update_selection()

    def load_screenshots(self):
        print("Loading screenshots...")
        self.screenshot_items = []
        self.screenshot_paths = []

        screenshot_folder = f"{current_path}/screenshots"
        
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
            
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        files = os.listdir(screenshot_folder)
        screenshot_files = [f for f in files if os.path.splitext(f)[1].lower() in valid_extensions]
        
        for widget in self.screenshot_scroll_frame.winfo_children():
            widget.destroy()

        for file in screenshot_files:
            screenshot_path = f"{screenshot_folder}/{file}"
            self.screenshot_paths.append(screenshot_path)

            try:
                pil_img = Image.open(screenshot_path)
                pil_img.thumbnail((int(self.master.winfo_screenwidth() * 0.06), int(self.master.winfo_screenheight() * 0.05)))
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img,
                                    size=(int(self.master.winfo_screenwidth() * 0.06), int(self.master.winfo_screenheight() * 0.05)))
            except Exception as e:
                ctk_img = None

            btn = ctk.CTkButton(
                self.screenshot_scroll_frame,
                text=file[:15] + "..." if len(file) > 15 else file,
                image=ctk_img,
                anchor="w",
                compound="left",
                height=int(self.master.winfo_screenheight() * 0.07),
                fg_color="#252525",
                hover_color="#353535",
                font=("Orbitron", 12),
                command=lambda path=screenshot_path, idx=len(self.screenshot_items): self.select_screenshot(idx)
            )
            btn.pack(pady=8, padx=10, fill="x")
            self.screenshot_items.append(btn)

    def switch_tab(self, tab_name):
        self.sounds["tab"].play()
        self.current_tab = tab_name
        
        accent_color = "#FF5722"
        highlight_color = "#2196F3"
        
        for i, name in enumerate(self.tabs):
            self.tab_buttons[i].configure(
                fg_color="#252525" if name != tab_name else accent_color,
                hover_color="#303030" if name != tab_name else highlight_color
            )
        
        if tab_name == "GAMES":
            self.scroll_frame.place(relx=0.02, rely=0.52, anchor="w", relwidth=0.28, relheight=0.75)
            self.screenshot_scroll_frame.place_forget()
            self.games_title.configure(text="GAME LIBRARY")
        else:
            self.load_screenshots()
            self.scroll_frame.place_forget()
            self.screenshot_scroll_frame.place(relx=0.02, rely=0.52, anchor="w", relwidth=0.28, relheight=0.75)
            self.games_title.configure(text="SCREENSHOTS")
        
        self.update_selection()

    def previous_tab(self, event=None):
        current_index = self.tabs.index(self.current_tab)
        new_index = (current_index - 1) % len(self.tabs)
        self.switch_tab(self.tabs[new_index])

    def next_tab(self, event=None):
        current_index = self.tabs.index(self.current_tab)
        new_index = (current_index + 1) % len(self.tabs)
        self.switch_tab(self.tabs[new_index])

    def delete_screenshot(self, event=None):
        if self.current_tab != "SCREENSHOTS" or not self.screenshot_paths or self.screenshot_selected_index >= len(self.screenshot_paths):
            return
            
        screenshot_path = self.screenshot_paths[self.screenshot_selected_index]
        file_name = os.path.basename(screenshot_path)
        
        self.confirm_dialog = ctk.CTkToplevel(self)
        self.confirm_dialog.title("Confirm Deletion")
        self.confirm_dialog.geometry("400x150")
        self.confirm_dialog.resizable(False, False)
        self.confirm_dialog.configure(fg_color="#1A1A1A")
        
        self.confirm_dialog.transient(self)
        self.confirm_dialog.grab_set()
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (400 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (150 // 2)
        self.confirm_dialog.geometry(f"+{x}+{y}")
        
        message_label = ctk.CTkLabel(
            self.confirm_dialog,
            text=f"Are you sure you want to delete:\n{file_name}?",
            font=("Orbitron", 14),
            text_color="#FFFFFF"
        )
        message_label.pack(pady=20)
        
        button_frame = ctk.CTkFrame(self.confirm_dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        self.dialog_selection = 0
        
        button_width = 100
        button_height = 35
        
        self.no_button = ctk.CTkButton(
            button_frame,
            text="No",
            font=("Orbitron", 12, "bold"),
            fg_color="#FF5722",
            hover_color="#FF7043",
            corner_radius=10,
            width=button_width,
            height=button_height,
            command=lambda: self.confirm_dialog.destroy()
        )
        self.no_button.pack(side="left", padx=10)
        
        self.yes_button = ctk.CTkButton(
            button_frame,
            text="Yes",
            font=("Orbitron", 12, "bold"),
            fg_color="#252525",
            hover_color="#303030",
            corner_radius=10,
            width=button_width,
            height=button_height,
            command=lambda: self.delete_confirmed(screenshot_path)
        )
        self.yes_button.pack(side="left", padx=10)
        
        self.confirm_dialog.bind("<KeyPress-a>", self.dialog_previous)
        self.confirm_dialog.bind("<KeyPress-d>", self.dialog_next)
        self.confirm_dialog.bind("<KeyPress-space>", self.dialog_select)
        self.confirm_dialog.bind("<KeyPress-Escape>", lambda e: self.confirm_dialog.destroy())
        
        self.update_dialog_selection()

    def update_dialog_selection(self):
        if hasattr(self, 'confirm_dialog') and self.confirm_dialog.winfo_exists():
            if self.dialog_selection == 0:
                self.no_button.configure(fg_color="#FF5722")
                self.yes_button.configure(fg_color="#252525")
            else:
                self.no_button.configure(fg_color="#252525")
                self.yes_button.configure(fg_color="#FF5722")

    def dialog_previous(self, event=None):
        self.dialog_selection = 0
        self.update_dialog_selection()

    def dialog_next(self, event=None):
        self.dialog_selection = 1
        self.update_dialog_selection()

    def dialog_select(self, event=None):
        if hasattr(self, 'confirm_dialog') and self.confirm_dialog.winfo_exists():
            if self.dialog_selection == 0:
                self.confirm_dialog.destroy()
            else:
                screenshot_path = self.screenshot_paths[self.screenshot_selected_index]
                self.delete_confirmed(screenshot_path)

    def delete_confirmed(self, path):
        try:
            os.remove(path)
            
            if hasattr(self, 'confirm_dialog') and self.confirm_dialog.winfo_exists():
                self.confirm_dialog.destroy()
                
            self.load_screenshots()
            
            if not self.screenshot_items:
                self.screenshot_selected_index = 0
            elif self.screenshot_selected_index >= len(self.screenshot_items):
                self.screenshot_selected_index = len(self.screenshot_items) - 1
                
            self.update_selection()
            
        except Exception as e:
            if hasattr(self, 'confirm_dialog') and self.confirm_dialog.winfo_exists():
                error_label = ctk.CTkLabel(
                    self.confirm_dialog,
                    text=f"Error: {str(e)}",
                    font=("Orbitron", 12),
                    text_color="#FF0000"
                )
                error_label.pack(pady=10)

    def display_screenshot(self, path):
        try:
            file_name = os.path.basename(path)
            self.game_title.configure(text=file_name[:25] + "..." if len(file_name) > 25 else file_name)
            
            pil_img = Image.open(path)
            img_width, img_height = pil_img.size
            display_width = int(self.master.winfo_screenwidth() * 0.6)
            display_height = int(self.master.winfo_screenheight() * 0.4)
            
            width_ratio = display_width / img_width
            height_ratio = display_height / img_height
            scale_factor = min(width_ratio, height_ratio)
            
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(new_width, new_height))
            self.image_label.configure(image=ctk_img)
            
            file_size = os.path.getsize(path) / 1024
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
            for i, button in enumerate(self.items):
                if i == self.games_selected_index:
                    button.set_selected(True)
                    game_name = button.cget('text')

                    self.game_title.configure(text=game_name.upper())

                    image_path = f"{current_path}/games/games_images/{game_name}.jpg"
                    image_width = int(self.master.winfo_screenwidth() * 0.6)
                    image_height = int(self.master.winfo_screenheight() * 0.4)

                    threading.Thread(
                        target=self.fade_image,
                        args=(image_path, image_width, image_height),
                        daemon=True
                    ).start()

                    text = self.read_txt(game_name)
                    self.desc_label.configure(
                        text=text,
                        justify="left"
                    )

                    button.update_idletasks()
                    scroll_frame_height = self.scroll_frame.winfo_height()
                    button_height = button.winfo_height()
                    button_y = button.winfo_y()

                    button_center = button_y + button_height / 2
                    scroll_fraction = (button_center - scroll_frame_height / 2) / (len(self.items) * button_height)
                    scroll_fraction = max(0, min(scroll_fraction, 1))

                    current_scroll = self.scroll_frame._parent_canvas.yview()[0]
                    self.animate_scroll(current_scroll, scroll_fraction, self.scroll_frame)
                    self.animate_slide_in()
                else:
                    button.set_selected(False)

        else:
            for i, button in enumerate(self.screenshot_items):  
                if i == self.screenshot_selected_index:
                    button.configure(fg_color="#0D6EFD",
                    border_color="#0A58CA",
                    hover_color="#1A74E9",
                    text_color="#FFFFFF")
                    if self.screenshot_paths and self.screenshot_selected_index < len(self.screenshot_paths):
                        screenshot_path = self.screenshot_paths[self.screenshot_selected_index]
                        self.display_screenshot(screenshot_path)

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
                    button.configure(fg_color="#252525", hover_color="#353535")

    def animate_scroll(self, start, end, frame=None):
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

    def animate_slide_in(self):
        target_relx = 0.33
        current_relx = self.right_content.place_info().get('relx')
        if current_relx is None:
            current_relx = 1.0
        else:
            current_relx = float(current_relx)

        distance = target_relx - current_relx
        steps = 10
        step_size = distance / steps

        def step(current_step):
            if current_step <= steps:
                new_relx = current_relx + (step_size * current_step)
                self.right_content.place(relx=new_relx)
                self.after(15, lambda: step(current_step + 1))

        step(1)

    def fade_image(self, new_image_path, target_width, target_height):
        try:
            new_image = Image.open(new_image_path)
            new_image = new_image.resize((target_width, target_height), Image.LANCZOS)

            # Fade out
            for i in range(10, -1, -1):
                alpha = i / 10
                if hasattr(self, "_current_image_pil"):
                    faded_image = Image.blend(self._current_image_pil, Image.new('RGBA', self._current_image_pil.size, (0,0,0,0)), 1 - alpha)
                    faded_tk = ImageTk.PhotoImage(faded_image)
                    self.image_label.configure(image=faded_tk)
                    self.update()
                    time.sleep(0.02)

            self._current_image_pil = new_image.convert("RGBA")

            # Fade in
            for i in range(11):
                alpha = i / 10
                faded_image = Image.blend(Image.new('RGBA', self._current_image_pil.size, (0,0,0,0)), self._current_image_pil, alpha)
                faded_tk = ImageTk.PhotoImage(faded_image)
                self.image_label.configure(image=faded_tk)
                self.update()
                time.sleep(0.02)

        except FileNotFoundError:
            self.image_label.configure(image=None, text="Image not found")
        except Exception as e:
            print(f"Error fading image: {e}")
            self.image_label.configure(image=None, text="Error loading image")

    def move_up(self, event):
        self.sounds["navigate"].play()
        if self.current_tab == "GAMES":
            if self.games_selected_index > 0:
                self.games_selected_index -= 1
                self.update_selection()
        else:
            if self.screenshot_selected_index > 0:
                self.screenshot_selected_index -= 1
                self.update_selection()

    def move_down(self, event):
        self.sounds["navigate"].play()
        if self.current_tab == "GAMES":
            if self.games_selected_index < len(self.items) - 1:
                self.games_selected_index += 1
                self.update_selection()
        else:
            if self.screenshot_selected_index < len(self.screenshot_items) - 1:
                self.screenshot_selected_index += 1
                self.update_selection()
    
    def select_item(self, event=None):
        self.sounds["select"].play()
        if self.current_tab == "GAMES":
            if self.items and self.games_selected_index < len(self.items):
                game_name = self.items[self.games_selected_index].cget("text")
                game_info = self.games_dict.get(game_name)
            
                self.update()
                
                if game_info:
                    game_path = game_info["path"]
                    launch_success = False
                    
                    try:
                        if game_info["type"] == "python":
                            subprocess.Popen(["python", game_path], 
                                            stderr=subprocess.PIPE,
                                            stdout=subprocess.PIPE)
                            launch_success = True
                            
                        elif game_info["type"] == "emulator":
                            subprocess.Popen(["/usr/games/mgba-qt", game_path],
                                            stderr=subprocess.PIPE,
                                            stdout=subprocess.PIPE)
                            launch_success = True
                            
                        if launch_success:
                            pass
                        else:
                            self.show_notification(f"Failed to launch {game_name}", "error")
                            
                    except Exception as e:
                        error_msg = str(e)
                        self.show_notification(f"Error launching {game_name}: {error_msg}", "error")
                                        
                self.last_select_item = time.time()

        else:
            if self.screenshot_paths and self.screenshot_selected_index < len(self.screenshot_paths):
                self.display_screenshot(self.screenshot_paths[self.screenshot_selected_index])

    def show_notification(self, message, notification_type="info"):
        colors = {
            "info": "#2196F3",
            "success": "#4CAF50",
            "error": "#F44336"
        }
        
        if hasattr(self, 'notification_frame'):
            self.notification_frame.destroy()
            
        self.notification_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=colors.get(notification_type, "#2196F3"),
            corner_radius=10,
            height=40
        )
        self.notification_frame.place(relx=0.5, rely=0.95, anchor="center", relwidth=0.3)
        
        notification_label = ctk.CTkLabel(
            self.notification_frame,
            text=message,
            font=("Orbitron", 14, "bold"),
            text_color="#FFFFFF"
        )
        notification_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.after(3000, lambda: self.notification_frame.destroy() if hasattr(self, 'notification_frame') else None)


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Center")
        self.attributes('-fullscreen', True)
        self.configure(fg_color="black")
        self.configure(cursor="none")
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        self.closing = 0
        self.last_closing_attempt = time.time()
        self.main_ui = None

        self.background = AnimatedBackground(self)
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Initialize pygame mixer
        pygame.mixer.init()
        self.sounds = {
            "navigate": pygame.mixer.Sound(f"{current_path}/assets/sounds/navigate.wav"),
            "select": pygame.mixer.Sound(f"{current_path}/assets/sounds/select.wav"),
            "tab": pygame.mixer.Sound(f"{current_path}/assets/sounds/tab.wav")
        }

        self.listener = subprocess.Popen(["sudo","python3",f"{current_path}/src/gpio_listener.py"])

        self.splash_screen = SplashScreen(self, on_close=self.show_main_ui)
        self.bind("<Escape>", self.close_window)

    def show_main_ui(self):
        self.splash_screen.destroy()
        self.main_ui = MainUI(self, self.sounds)
        self.main_ui.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.background.lower()
        self.main_ui.lift()
        self.fade_in_main()
        self.set_focus()

        # Bind keys to MainUI methods
        self.bind("<KeyPress-w>", self.main_ui.move_up)
        self.bind("<KeyPress-s>", self.main_ui.move_down)
        self.bind("<KeyPress-a>", self.main_ui.previous_tab)
        self.bind("<KeyPress-d>", self.main_ui.next_tab)
        self.bind("<KeyPress-space>", self.main_ui.select_item)
        self.bind("<KeyPress-f>", self.main_ui.delete_screenshot)

    def set_focus(self):
        self.focus_force()
        self.attributes('-topmost',True)
        self.attributes('-fullscreen',True)
        self.after(2000, lambda: os.system("xdotool search --name 'Game Center' windowactivate"))
        self.update_idletasks()

    def fade_in_main(self):
        for i in range(0, 101, 2):
            self.attributes('-alpha', i/100)
            self.update()
            time.sleep(0.01)

    def close_window(self, event):
        current_time = time.time()
        time_diff = current_time - self.last_closing_attempt
        
        if time_diff >= 1:
            self.closing = 0
            
        self.closing += 1
        if self.closing >= 10:
            self.quit() 
            self.listener.terminate()
            self.listener.wait()
            
        self.last_closing_attempt = current_time

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
