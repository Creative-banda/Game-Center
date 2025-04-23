# Run this Script to install all the necessary libs and deps 

import subprocess
import sys

# Function to execute commands and check for success
def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing: {command}")
        print(e)
        sys.exit(1)

# Updating system packages
def update_system():
    print("Updating system packages...")
    run_command("sudo apt update && sudo apt upgrade -y")

# Installing Python & Pip
def install_python_pip():
    print("Installing Python 3 and Pip...")
    run_command("sudo apt install python3 -y")
    run_command("sudo apt install python3-pip -y")
    run_command("sudo python3 -m pip install --upgrade pip")

# Installing required libraries
def install_libraries():
    print("Installing required libraries...")

    libraries = [
        "python3-tk",
        "python3-dev",
        "libsdl2-dev",
        "libsdl2-image-dev",
        "libsdl2-mixer-dev",
        "libsdl2-ttf-dev",
        "libfreetype6-dev",
        "libportmidi-dev",
        "libjpeg-dev",
        "python3-rpi.gpio",
        "xdotool",
        "git",
        "mgba-qt"
    ]

    for lib in libraries:
        run_command(f"sudo apt install {lib} -y")

    # Install Python packages via pip
    pip_packages = [
        "customtkinter",
        "keyboard",
        "socket",
        "pygame"
    ]
    for package in pip_packages:
        run_command(f"sudo pip3 install {package} --break-system-packages")

# Verifying installation
def verify_installation():
    print("Verifying installation...")
    try:
        import pygame, customtkinter, RPi.GPIO, socket, keyboard
        print("All libraries installed successfully!")
    except ImportError as e:
        print("Failed to import some libraries. Please check the installation process.")
        print(e)
        sys.exit(1)

# Main installation function
def main():
    print("Starting installation script...")

    update_system()
    install_python_pip()
    install_libraries()
    verify_installation()

    print("Installation completed successfully! Now, please configure the gamecenter.service manually.")

if __name__ == "__main__":
    main()
