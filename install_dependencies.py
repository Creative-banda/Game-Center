# Run this Script to install all the necessary libs and deps 

import subprocess
import sys
from time import sleep


user = ""
path = ""

def setup_user_and_path():
    global user, path
    print("🔧 Let's configure Game Center on your Raspberry Pi")
    print("\n👉 Enter your Raspberry Pi username.")
    print("   (This is usually 'pi' unless you've set a custom user)")
    user = input("Username: ").strip()

    print("\n👉 Enter the full path to the Game Center folder.")
    print("You can find the path where you clone the repo.")
    print("     Example: /home/pi/GameCenter")
    path = input("Full path: ").strip()

# Function to execute commands and check for success
def run_command(command):
    try:
        print(f"Running command: {command}") 
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
        "pygame"
    ]
    for package in pip_packages:
        run_command(f"sudo pip3 install {package} --break-system-packages")

# Troubleshooting PIL issues    
def trouble_shooting():
    print("Checking and fixing PIL issues if any...")
    try:
        run_command("sudo apt install --reinstall python3-pil python3-tk")
        run_command("pip install --break-system-packages --upgrade --force-reinstall pillow")
    except Exception as e:
        print(f"\n⚠️  Uh-oh! Troubleshooting failed: {e}")  
        print("   🛠️  Try these commands to fix things:")  
        print("""   
            📝 Run these one by one:  
            sudo apt install --reinstall python3-pil python3-tk  
            pip install --break-system-packages --upgrade --force-reinstall pillow  
            """)  
        print("   🔧 If the issue persists, check the troubleshooting guide.")
           
# Create Service
def create_service():
    global user, path

    service_content = f"""[Unit]
    Description=Game Center GUI Application
    After=multi-user.target

    [Service]
    User={user}
    Group={user}
    WorkingDirectory={path}
    ExecStart=/usr/bin/python3 {path}/main.py
    Environment=DISPLAY=:0
    Restart=always

    [Install]
    WantedBy=multi-user.target
    """

    try:
        # Save to a temporary file
        with open("gamecenter.service", "w") as f:
            f.write(service_content)

        # Move the file and enable service
        subprocess.run(["sudo", "mv", "gamecenter.service", "/etc/systemd/system/gamecenter.service"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "gamecenter.service"], check=True)

        print("\n✅ Game Center will now launch automatically at startup! 🚀")  
        print("   🔧 Run into trouble? Check the troubleshooting guide for help.")  
        print("   ℹ️  Want to check if it's running? Use: `sudo systemctl status gamecenter.service`")  
    except Exception as e:  
        print("\n❌ Oops! Something went wrong:")  
        print(f"   🔍 Error: {e}")  
        print("   🛠️  Double-check the service file and try again.")  

# Verifying installation
def verify_installation():
    print("🔍 Checking if all libraries are installed...")  
    try:  
        import pygame, customtkinter, RPi.GPIO, keyboard  
        print("🎉 All good! Libraries are ready to go!")  
    except ImportError as e:  
        print("\n❌ Whoops! Missing some libraries.")  
        print(f"   🔍 Error: {e}")  
        print("   🛠️  Re-run the installer or check the setup guide.")  
        sys.exit(1)  
        
def reboot_system():  
    confirm = input("\n🔁 Reboot now to apply changes? Press y to reboot ").strip().lower()  
    if confirm == "y" or confirm == "Y":  
        print("\n🔄 Rebooting now... See you in a sec! ⚡")  
        sleep(1)
        subprocess.run(["sudo", "reboot"])  
    else:  
        print("\nℹ️  No worries! You can reboot later with: `sudo reboot`")  

# Main installation function
def main():
    setup_user_and_path()
    update_system()
    install_python_pip()
    install_libraries()
    trouble_shooting()
    create_service()
    verify_installation()
    reboot_system()

    print("\n🎉 Game Center is all set up and ready to rock! 🎮")  
    print("   🔧 Need help? Check the troubleshooting section for tips.")  

if __name__ == "__main__":
    main()
