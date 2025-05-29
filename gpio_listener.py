# Import necessary libraries


import RPi.GPIO as GPIO
import time, os, getpass, keyboard
import subprocess
from pathlib import Path

from utils.env_utils import get_display_env, get_env_for_screenshot, take_screenshot

env, _ = get_display_env()


screenshot_env = get_env_for_screenshot()

# Get the current script's directory
current_path = Path(__file__).parent.resolve()

# Define GPIO pin mappings
PIN_MAPPING = {
    6: ["w", "up"],  # LEFT_HAND_UP → W + UP
    12: ["s", "down"],  # LEFT_HAND_DOWN → S + DOWN
    13: ["a", "left"],  # LEFT_HAND_LEFT → A + LEFT
    19: ["d", "right"],  # LEFT_HAND_RIGHT → D + RIGHT
    16: ["space"],  # RIGHT_HAND_UP → SPACEBAR
    26: ["q"],  # RIGHT_HAND_LEFT → Q
    20: ["f"],  # RIGHT_HAND_RIGHT → F
    21: ["p"],  # RIGHT_HAND_DOWN → P
    5: ["alt", "f4"]  # TOP_BUTTON → ALT + F4
}

# Define special key combinations
KEY_COMBINATIONS = {
    (6, 12, 16): ["f1"],  # LEFT_HAND_UP + LEFT_HAND_DOWN + RIGHT_HAND_UP  → F1
    (6, 12, 20): ["shift", "f1"],  # LEFT_HAND_UP + LEFT_HAND_DOWN + RIGHT_HAND_RIGHT → Shift + F1
    (6, 12, 21): ["enter"],  # LEFT_HAND_UP + LEFT_HAND_DOWN + RIGHT_HAND_DOWN → Return(Enter)
    (6, 12, 26): ["ctrl", "f"], # LEFT_HAND_UP + LEFT_HAND_DOWN + RIGHT_HAND_LEFT → CTRL + F
    (13, 19, 16): "screenshot", # LEFT_HAND_LEFT + LEFT_HAND_RIGHT + RIGHT_HAND_UP → Screenshot
}


last_screenshot = 0  # Initialize last_screenshot to 0


# GPIO Setup
GPIO.setmode(GPIO.BCM)
for pin in PIN_MAPPING.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set as input with pull-up resistor

# Track pressed keys
pressed_keys = set()
active_combinations = set()

# Track shutdown button state
shutdown_pin = 5
shutdown_hold_start = None
shutdown_triggered = False


def gpio_listener():
    print("Listening for GPIO inputs... (Press Ctrl+C to stop)")
    global last_screenshot

    try:
        while True:
            active_pins = {pin for pin in PIN_MAPPING.keys() if GPIO.input(pin) == GPIO.LOW}
            
            # Handle special shutdown logic
            if shutdown_pin in active_pins:
                if shutdown_hold_start is None:
                    shutdown_hold_start = time.time()
                elif time.time() - shutdown_hold_start >= 3 and not shutdown_triggered:
                    print("Shutdown button held for 3 seconds. Shutting down...")
                    shutdown_triggered = True
                    try:
                        subprocess.Popen(["python3", f"{current_path}/show_shutdown_overlay.py"], env=env)
                        os.system("xdotool search --name 'Shutting Down' windowactivate")
                    except Exception as e:
                        print(f"Error starting shutdown overlay: {e}")
                        # Create a Log File
                        with open("shutdown_error.log", "a") as log_file:
                            log_file.write(f"Error: {e}\n")
                        os.system("sudo shutdown now")
            else:
                shutdown_hold_start = None
                shutdown_triggered = False

            # Handle combinations first
            handled_combinations = False  
            for combo, output in KEY_COMBINATIONS.items():
                if all(pin in active_pins for pin in combo):
                    if combo not in active_combinations:  # Only act if not already active
                        active_combinations.add(combo)
                        
                        if output == "screenshot":         
                            if time.time() - last_screenshot > 1:
                                print("Screenshot combination detected! 📸")
                                subprocess.Popen(["python3", f"{current_path}/screen_shot_layout.py"], env=env)
                                take_screenshot(screenshot_env)
                                last_screenshot = time.time()
                        
                        else:
                            for key in output:
                                keyboard.press(key)
                                pressed_keys.add(key)
                    handled_combinations = True
                elif combo in active_combinations:
                    if output != "screenshot":
                        for key in output:
                            keyboard.release(key)
                            pressed_keys.discard(key)
                    active_combinations.discard(combo)


            # Process regular key mappings ONLY if no combinations were handled
            if not handled_combinations:
                for pin in PIN_MAPPING:
                    if pin in active_pins:
                        for key in PIN_MAPPING[pin]:
                            if key not in pressed_keys:
                                keyboard.press(key)
                                pressed_keys.add(key)
                    else:  # Button released
                        for key in PIN_MAPPING[pin]:
                            if key in pressed_keys:
                                keyboard.release(key)
                                pressed_keys.discard(key)

            time.sleep(0.05)  # Small delay for performance optimization
    except KeyboardInterrupt:
        print("Stopping GPIO Listener...")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

# Run the listener
if __name__ == "__main__":
    gpio_listener()
