import pygame

class Button():
    def __init__(self, x, y, image, scale, key=None):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.key = key  # Keyboard key to listen for

    def draw(self, surface, events):
        action = False
        pos = pygame.mouse.get_pos()

        # Process events passed from the main loop
        for event in events:
            # Check if mouse button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
                if event.button == 1 and not self.clicked:  # Left click
                    action = True
                    self.clicked = True

            # Check if the assigned keyboard key is pressed
            if event.type == pygame.KEYDOWN and self.key is not None and event.key == self.key:
                action = True
                self.clicked = True  # Prevent multiple triggers

            # Reset click state when mouse button or key is released
            if event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYUP and self.key is not None and event.key == self.key):
                self.clicked = False

        # Draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
