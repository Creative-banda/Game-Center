import customtkinter as ctk

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
