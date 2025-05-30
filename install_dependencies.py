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
    print(" ****** 🔧 Configuring Game Center on your Raspberry Pi...")
    user = getpass.getuser()  # Get the current username
    path = str(Path(__file__).resolve().parent)  # Get the current script's directory
    print(f"Detected username: {user}")
    print(f"Detected path: {path}")

# Function to execute commands and check for success
import subprocess
import sys

def run_command(command):
    try:
        print(f"Running command: {command}")
        subprocess.check_call(
            command,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Error occurred while executing: {command}")
        print(f"🔍 {e}")
        sys.exit(1)


# Updating system packages
def update_system():
    print(" ****** Refreshing package list...")
    run_command("sudo apt update")


# Installing Python & Pip
def install_python_pip():
    print(" ****** Installing Python 3 and Pip...")
    run_command("sudo apt install python3-pip -y")

# Installing required libraries
def install_libraries():
    print(" ****** Installing required system libraries...")

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

    run_command(f"sudo apt install {' '.join(system_libraries)} -y")

    print(" ****** Installing required Python pip packages...")

    pip_packages = [
        "customtkinter",
        "keyboard",
        "pygame",
        "opencv-python",
        "Pillow",
    ]

    run_command(f"sudo pip3 install {' '.join(pip_packages)} --break-system-packages")


# Troubleshooting PIL issues    
def trouble_shooting():
    print(" ****** Checking and fixing PIL issues if any...")
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
        After=graphical.target multi-user.target user@1000.service
        Wants=graphical.target user@1000.service

        [Service]
        User={user}
        Group={user}
        RestartSec=2
        TimeoutStopSec=2
        KillSignal=SIGKILL
        SendSIGKILL=yes
        KillMode=control-group
        WorkingDirectory={path}
        ExecStart=/usr/bin/python3 {path}/main.py
        Environment=DISPLAY=:0
        Environment=XDG_RUNTIME_DIR=/run/user/1000
        Environment=XAUTHORITY=/home/{user}/.Xauthority
        Environment=PULSE_SERVER=/run/user/1000/pulse/native
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
        print(" ******    🔧 Run into trouble? Check the troubleshooting guide for help.")  
        print(" ******    ℹ️  Want to check if it's running? Use: `sudo systemctl status gamecenter.service`")  
    except Exception as e:  
        print("\n❌ Oops! Something went wrong:")  
        print(f"   🔍 Error: {e}")  
        print("   🛠️  Double-check the service file and try again.")  


def install_font():
    print(" ****** Installing custom font...")
    try:
        run_command("sudo mkdir -p /usr/share/fonts/truetype/orbitron")
        run_command(f"sudo cp {path}/fonts/Orbitron.ttf /usr/share/fonts/truetype/orbitron/")
        run_command("sudo fc-cache -f -v")
    except Exception as e:
        print(f"\n❌ Oops! Font installation failed: {e}")  
        print(" ****** 🛠️  Double-check the font path and try again.")  
    print("****** Font installation complete! 🎨")

# Setting up display mirroring for HDMI-1
def setup_display_mirroring():
    print("****** 📺 Setting up HDMI-1 as the primary display...")

    # Step 1: Create the display script
    display_script = """#!/bin/bash
        xrandr --output HDMI-1 --mode 800x480 --primary
        xrandr --output HDMI-2 --off
    """


    try:
        script_path = "/usr/local/bin/set-primary-display.sh"
        with open("set-primary-display.sh", "w") as f:
            f.write(display_script)

        run_command(f"sudo mv set-primary-display.sh {script_path}")
        run_command(f"sudo chmod +x {script_path}")
        print("****** ✅ Display control script created and made executable.")

        # Step 2: Create the systemd service file
        display_service = f"""[Unit]
            Description=Force HDMI-1 as primary display
            After=graphical.target

            [Service]
            ExecStart={script_path}
            Type=oneshot
            User={user}
            Environment=DISPLAY=:0
            Environment=XAUTHORITY=/home/{user}/.Xauthority

            [Install]
            WantedBy=graphical.target
            """
        with open("set-primary-display.service", "w") as f:
            f.write(display_service)

        run_command("sudo mv set-primary-display.service /etc/systemd/system/set-primary-display.service")
        run_command("sudo systemctl enable set-primary-display.service")
        print(" ****** ✅ Display service installed and enabled!")
        
        # Step 3: Create the udev rule for hotplugging
        hotplug_rule()
        print("****** 🔌 Setting up hotplug rule for HDMI display...")
        run_command("sudo udevadm control --reload-rules")
        run_command("sudo udevadm trigger")
        print(" ****** ✅ Hotplug rule created and reloaded!")
        
        # Step 4: Create the auto-mirror script
        auto_mirror_service()
        auto_mirror_timer()
        auto_mirror_display()
        
        print("****** ✅ Auto-mirror service created and enabled!")
        print("****** 📺 HDMI-1 is now set as the primary display and will mirror automatically!")

    except Exception as e:
        print("****** \n❌ Failed to set up display mirroring:")
        print(f"****** 🔍 Error: {e}")
        print("****** 🛠️  Double-check paths and permissions, then try again.")


def auto_mirror_display():
    
    service_content = """
    [Unit]
    Description=Mirror HDMI display dynamically
    After=graphical.target

    [Service]
    ExecStart=/usr/local/bin/auto-mirror.sh
    User=pi
    Environment=DISPLAY=:0
    Environment=XAUTHORITY=/home/pi/.Xauthority

    [Install]
    WantedBy=multi-user.target
    """
    with open("auto-mirror.service", "w") as f:
        f.write(service_content)

    run_command("sudo mv auto-mirror.service /etc/systemd/system/auto-mirror.service")
    run_command("sudo systemctl enable auto-mirror.service")
    print(" ****** ✅ Auto-mirror service installed and enabled!")

def auto_mirror_timer():
    script_content = """
    [Unit]
    Description=Run auto-mirror script a few seconds after boot

    [Timer]
    OnBootSec=15s
    Unit=auto-mirror.service

    [Install]
    WantedBy=multi-user.target
    """
    with open("auto-mirror.timer", "w") as f:
        f.write(script_content)
    
    run_command("sudo mv auto-mirror.timer /etc/systemd/system/auto-mirror.timer")
    run_command("sudo systemctl enable auto-mirror.timer")


def auto_mirror_service():
    script_content = """
    #!/bin/bash
    export DISPLAY=:0
    export XAUTHORITY=/home/pi/.Xauthority

    PRIMARY="HDMI-1"
    PRIMARY_RES="800x480"

    while true; do
        CONNECTED=$(xrandr | grep " connected" | awk '{print $1}')
        for DISPLAY_NAME in $CONNECTED; do
            if [ "$DISPLAY_NAME" != "$PRIMARY" ]; then
                RES=$(xrandr | grep -A1 "^$DISPLAY_NAME connected" | tail -n1 | awk '{print $1}')
                xrandr --output "$DISPLAY_NAME" --mode "$RES" --scale-from "$PRIMARY_RES" --same-as "$PRIMARY"
                exit 0
            fi
        done
        sleep 1
    done
    """
    with open("auto-mirror.sh", "w") as f:
        f.write(script_content)
    run_command("sudo mv auto-mirror.sh /usr/local/bin/auto-mirror.sh")
    run_command("sudo chmod +x /usr/local/bin/auto-mirror.sh")

def hotplug_rule():
    content = """
    SUBSYSTEM=="drm", ACTION=="change", RUN+="/usr/local/bin/auto-mirror.sh"
    """
    with open("99-hdmi-hotplug.rules", "w") as f:
        f.write(content)
    run_command("sudo mv 99-hdmi-hotplug.rules /etc/udev/rules.d/99-hdmi-hotplug.rules")

# Verifying installation
def verify_installation():
    print(" ****** 🔍 Checking if all libraries are installed...")  
    try:  
        import pygame, customtkinter, RPi.GPIO, keyboard  
        print(" ****** 🎉 All good! Libraries are ready to go!")  
    except ImportError as e:  
        print("\n❌ Whoops! Missing some libraries.")  
        print(f"   🔍 Error: {e}")  
        print(" ******    🛠️  Re-run the installer or check the setup guide.")  
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
    setup_display_mirroring()
    verify_installation()
    install_font()
    reboot_system()

    print("\n🎉 Game Center is all set up and ready to rock! 🎮")  
    print(" ******    🔧 Need help? Check the troubleshooting section for tips.")  

if __name__ == "__main__":
    main()
