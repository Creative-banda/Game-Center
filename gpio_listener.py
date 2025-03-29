import RPi.GPIO as GPIO
import time
import keyboard  # To simulate keypress events

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
    (6, 16): ["f1"],  # W (UP) + P (RIGHT HAND DOWN) → F1
    (12, 21): ["shift", "f1"],  # S (DOWN) + RIGHT_HAND_UP (Q) → SHIFT + F1
    (13, 19): ["enter"],
}

# GPIO Setup
GPIO.setmode(GPIO.BCM)
for pin in PIN_MAPPING.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set as input with pull-up resistor

# Track pressed keys
pressed_keys = set()
active_combinations = set()

def gpio_listener():
    print("Listening for GPIO inputs... (Press Ctrl+C to stop)")
    try:
        while True:
            active_pins = {pin for pin in PIN_MAPPING.keys() if GPIO.input(pin) == GPIO.LOW}

            # Handle combinations first
            handled_combinations = False  
            for combo, output_keys in KEY_COMBINATIONS.items():
                if all(pin in active_pins for pin in combo):
                    if combo not in active_combinations:  # Only press keys if not already active
                        active_combinations.add(combo)
                        for key in output_keys:
                            keyboard.press(key)
                            pressed_keys.add(key)
                    handled_combinations = True
                elif combo in active_combinations:  # If combo is no longer pressed, release keys
                    for key in output_keys:
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
