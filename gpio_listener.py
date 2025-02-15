import RPi.GPIO as GPIO
import time
import keyboard  # To simulate keypress events

# Define GPIO pin mappings
PIN_MAPPING = {
    26: ["w"],  # LEFT_HAND_UP → W
    19: ["s"],  # LEFT_HAND_DOWN → S
    13: ["a"],  # LEFT_HAND_LEFT → A
    6: ["d"],   # LEFT_HAND_RIGHT → D
    21: ["space"],  # RIGHT_HAND_UP → SPACEBAR
    16: ["q"],  # RIGHT_HAND_LEFT → Q
    12: ["f"],  # RIGHT_HAND_RIGHT → F
    20: ["ctrl", "f4"]  # RIGHT_HAND_DOWN → CTRL + F4
}

# GPIO Setup
GPIO.setmode(GPIO.BCM)
for pin in PIN_MAPPING.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set as input with pull-up resistor

# Track pressed keys
pressed_keys = set()

def gpio_listener():
    print("Listening for GPIO inputs... (Press Ctrl+C to stop)")
    try:
        while True:
            for pin, keys in PIN_MAPPING.items():
                if GPIO.input(pin) == GPIO.LOW:  # Button is pressed
                    for key in keys:
                        if key not in pressed_keys:  # Prevent duplicate presses
                            keyboard.press(key)
                            pressed_keys.add(key)
                else:  # Button is released
                    for key in keys:
                        if key in pressed_keys:
                            keyboard.release(key)
                            pressed_keys.remove(key)

            time.sleep(0.05)  # Small delay for performance optimization
    except KeyboardInterrupt:
        print("Stopping GPIO Listener...")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

# Run the listener
if __name__ == "__main__":
    gpio_listener()
