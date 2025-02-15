import RPi.GPIO as GPIO
import time
import keyboard  # To simulate keypress events

# Define GPIO pin mappings
PIN_MAPPING = {
    26: "w",  # LEFT_HAND_UP → W
    19: "s",  # LEFT_HAND_DOWN → S
    13: "a",  # LEFT_HAND_LEFT → A
    6: "d",   # LEFT_HAND_RIGHT → D
    21: "space",  # RIGHT_HAND_UP → SPACEBAR
    16: "q",  # RIGHT_HAND_LEFT → E (assigned manually)
    12: "f",  # RIGHT_HAND_RIGHT → F (assigned manually)
    20: "p"  # RIGHT_HAND_DOWN → (Reserved, does nothing for now)
}

# GPIO Setup
GPIO.setmode(GPIO.BCM)
for pin in PIN_MAPPING.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set as input with pull-up resistor

# Function to listen for button presses
def gpio_listener():
    print("Listening for GPIO inputs... (Press Ctrl+C to stop)")
    try:
        while True:
            for pin, key in PIN_MAPPING.items():
                if key and GPIO.input(pin) == GPIO.LOW:  # Button pressed
                    keyboard.press(key)
                    time.sleep(0.2)  # Small delay to prevent repeated presses
                    keyboard.release(key)
    except KeyboardInterrupt:
        print("Stopping GPIO Listener...")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

# Run the listener
if __name__ == "__main__":
    gpio_listener()
