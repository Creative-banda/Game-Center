# Run this Script to install all the necessary libs and deps 

import subprocess
import sys
from time import sleep
from pathlib import Path
import getpass


user = ""
path = ""

def setup_user_and_path():
    global user, path
    print("🔧 Configuring Game Center on your Raspberry Pi...")
    user = getpass.getuser()  # Get the current username
    path = str(Path(__file__).resolve().parent)  # Get the current script's directory
    print(f"Detected username: {user}")
    print(f"Detected path: {path}")

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
    print("Refreshing package list...")
    run_command("sudo apt update")


# Installing Python & Pip
def install_python_pip():
    print("Installing Python 3 and Pip...")
    run_command("sudo apt install python3-pip -y")

# Installing required libraries
def install_libraries():
    print("Installing required system libraries...")

    system_libraries = [
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
        "mgba-qt",
        "grim",
    ]

    # Install all system libraries in one command
    run_command(f"sudo apt install {' '.join(system_libraries)} -y")

    print("Installing required Python pip packages...")

    pip_packages = [
        "customtkinter",
        "keyboard",
        "pygame",
        "opencv-python",
        "Pillow",
    ]

    # Install all pip packages in one command
    run_command(f"sudo pip3 install {' '.join(pip_packages)} --break-system-packages")


# Troubleshooting PIL issues    
def trouble_shooting():
    print("Checking and fixing PIL issues if any...")
    try:
        run_command("sudo apt install --reinstall python3-pil python3-tk")
        run_command("pip3 install --break-system-packages --upgrade --force-reinstall pillow")
    except Exception as e:
        print(f"\n⚠️  Uh-oh! Troubleshooting failed: {e}")  
        print("   🛠️  Try these commands to fix things:")  
        print("""   
            📝 Run these one by one:  
            sudo apt install --reinstall python3-pil python3-tk  
            pip3 install --break-system-packages --upgrade --force-reinstall pillow  
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


def install_font():
    print("Installing custom font...")
    try:
        run_command("sudo mkdir -p /usr/share/fonts/truetype/orbitron")
        run_command(f"sudo cp {path}/fonts/Orbitron.ttf /usr/share/fonts/truetype/orbitron/")
        run_command("sudo fc-cache -f -v")
    except Exception as e:
        print(f"\n❌ Oops! Font installation failed: {e}")  
        print("   🛠️  Double-check the font path and try again.")  
    print("Font installation complete! 🎨")

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
    install_font()
    reboot_system()

    print("\n🎉 Game Center is all set up and ready to rock! 🎮")  
    print("   🔧 Need help? Check the troubleshooting section for tips.")  

if __name__ == "__main__":
    main()
