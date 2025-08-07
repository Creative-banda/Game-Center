import customtkinter as ctk
import tkinter as tk
import random

class AnimatedBackground(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="black")
        self.master = master
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.stars = []
        self.num_stars = 150

        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.canvas.config(width=self.width, height=self.height)

        for _ in range(self.num_stars):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            size = random.uniform(1, 3)
            speed = random.uniform(0.1, 1)
            self.stars.append([x, y, size, speed])

        self.animate()

    def animate(self):
        self.canvas.delete("all")
        for star in self.stars:
            star[1] += star[3]  # Move star down
            if star[1] > self.height:
                star[0] = random.uniform(0, self.width)
                star[1] = 0

            self.canvas.create_oval(
                star[0], star[1], star[0] + star[2], star[1] + star[2],
                fill="white", outline=""
            )
        self.master.after(30, self.animate)

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
                fg_color="#202020",
                border_color="#FFA726",  # Highlight color for glow effect
                hover_color="#2D2D2D",
                text_color="#FFA726"
            )
        else:
            self.configure(
                fg_color="#202020",
                border_color="#333333",
                hover_color="#2D2D2D",
                text_color="#EDEDED"
            )
