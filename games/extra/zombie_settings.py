import pygame
from pathlib import Path


pygame.display.init()
pygame.mixer.init()



# Virtual Resolution (Logical Resolution for Game Logic)
VIRTUAL_WIDTH = 800
VIRTUAL_HEIGHT = 600

# Get Actual Screen Resolution
actual_screen_width, actual_screen_height = pygame.display.get_desktop_sizes()[0]


# Testing Resolution
# actual_screen_width = 800
# actual_screen_height = 600


# Scaling Factors
scale_x = actual_screen_width / VIRTUAL_WIDTH
scale_y = actual_screen_height / VIRTUAL_HEIGHT

CELL_SIZE_SCALED = 45 * scale_x
COLLECT_ITEM_SIZE_SCALED = 20 * scale_x

# General Settings
FPS = 70
MAX_LEVEL = 3  # Maximum number of levels in the game

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Sizes
PLAYER_SIZE = int(30 * scale_x) 
BULLET_SIZE = int(2 * scale_x)
BULLET_SPEED = int(7 * scale_x)
ZOMBIE_SIZE = int(35 * scale_x)
ZOMBIE_SPEED = int(1 * scale_x)

TORCH_RADIUS = int(180 * scale_x)

PLAYER_SPEED = int(2*scale_x)

# Get the script's directory
current_path = Path(__file__).parent

# Move up one level to remove "extra"
parent_path = current_path.parent

# Correct ASSETS_DIR
ASSETS_DIR = parent_path / "zombie_assets"

IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sound_effect"
LEVELS_DIR = ASSETS_DIR / "levels"

# Debugging path
print(f"IMAGES_DIR: {IMAGES_DIR / 'bullet.png'}")


# Asset Files
bullet_image = pygame.image.load(IMAGES_DIR / "bullet.png")
health_image = pygame.image.load(IMAGES_DIR / "health.png")
akm_image = pygame.image.load(IMAGES_DIR / "AKM.png")
rifle_ammo_image = pygame.image.load(IMAGES_DIR / "rifle_ammo.png")
shotgun_image = pygame.image.load(IMAGES_DIR / "shotgun.png")
shotgun_ammo_image = pygame.image.load(IMAGES_DIR / "shotgun_bullet.png")
piston_ammo_image = pygame.image.load(IMAGES_DIR / "piston_bullet.png")
bg_image = pygame.image.load(IMAGES_DIR / "background.jpg")
wall_image = pygame.image.load(IMAGES_DIR / "wall.PNG")
breakable_wall_image = pygame.image.load(IMAGES_DIR / "break_wall.png")
dead_zombie_image = pygame.image.load(IMAGES_DIR / "dead_zombie.png")
dead_zombie_image = pygame.transform.scale(dead_zombie_image, (ZOMBIE_SIZE, ZOMBIE_SIZE))

# Sound Files
gun_pickup_sound = pygame.mixer.Sound(SOUNDS_DIR / "gun_pickup.mp3")
gun_pickup_sound.set_volume(0.5)

item_pickup_sound = pygame.mixer.Sound(SOUNDS_DIR / "collect_item.mp3")
item_pickup_sound.set_volume(0.5)

death_sound = pygame.mixer.Sound(SOUNDS_DIR / "death.mp3")
death_sound.set_volume(0.5)

victory_sound = pygame.mixer.Sound(SOUNDS_DIR / "victory_sound.mp3")
victory_sound.set_volume(0.5)

loose_sound = pygame.mixer.Sound(SOUNDS_DIR / "loose.mp3")
loose_sound.set_volume(0.5)

walk_sound = pygame.mixer.Sound(SOUNDS_DIR / 'player_walk.mp3')
walk_sound.set_volume(0.5)

background_music = pygame.mixer.Sound(f"{SOUNDS_DIR / 'background_music.mp3'}")
background_music.set_volume(0.5)


# Player Gun Info
gun_info = {
    "handgun": {
        "damage": 20,
        "ammo": 15,
        "magazine": 6,
        "cooldown": 0,
        "remaining_ammo": 6,
        "sound": SOUNDS_DIR / 'gun_sound/handgun.mp3',
        "reloading_sound" : SOUNDS_DIR / 'gun_sound/handgun_reload.mp3'
    },
    "rifle": {
        "damage": 50,
        "ammo": 40,
        "magazine": 20,
        "cooldown": 100,
        "remaining_ammo": 20,
        "sound": SOUNDS_DIR / 'gun_sound/rifle.mp3',
        "reloading_sound" : SOUNDS_DIR / 'gun_sound/rifle_reload.mp3'

    },
    "shotgun": {
        "damage": 100,
        "ammo": 10,
        "magazine": 2,
        "cooldown": 1000,
        "remaining_ammo": 2,
        "sound": SOUNDS_DIR / 'gun_sound/shotgun_shot.mp3',
        "reloading_sound" : SOUNDS_DIR / 'gun_sound/shotgun_reload.mp3'

    }
}
