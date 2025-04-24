# Game Center for Raspberry Pi

A customizable game center built with CustomTkinter, designed to launch automatically on Raspberry Pi startup.

## Features
- Modern and intuitive user interface
- Auto-launch capability on system startup
- Built using CustomTkinter for enhanced visual appeal
- Optimized for Raspberry Pi systems
- **Auto-update system** to keep the application up-to-date with the latest changes

---

---

### 1. Configure Raspberry Pi OS
#### Editing the Config File (Method 1: Terminal - Recommended)
```bash
sudo nano /boot/config.txt
```
Copy the `config.txt` file from the repository root folder and replace everything in your config file with its contents. Then, save the changes:
- Press `Ctrl + X`
- Press `Y`
- Hit `Enter`

#### Editing the Config File (Method 2: Using Another System)
If the Pi isn’t booting, remove the SD card, insert it into another computer, and find `config.txt` in the `/boot/` partition. Replace it with the new `config.txt` from the repository.

---

### 2. Clone the GitHub Repository
#### Install Git
Before cloning the repository, install Git if it’s not already installed:
```bash
sudo apt install git -y
```

#### Why We Need Git
Git allows us to download and manage the latest version of Game Center directly from the repository. This ensures we always have access to the newest features, bug fixes, and improvements. By using Git, we can easily update our application without manually downloading files. Additionally, our **auto-update system** relies on Git to fetch updates seamlessly.

#### Clone the Repository
To download the latest version of Game Center, clone the repository using Git:
```bash
git clone <REPO_URL>
```
Navigate into the project directory:
```bash
cd <REPO_FOLDER>
```
To pull updates in the future, run:
```bash
git pull
```

If you encounter permission issues while updating, try:
```bash
git reset --hard
```



## Installation Guide

### 🔧 Easy Installation Script(Automated)
To make the setup process easier, we've created an automated Python script that installs all required libraries and dependencies for Game Center. Instead of installing each package manually, simply run the script and let it handle everything for you. This ensures a smooth and hassle-free installation experience.
```bash
python3 install_dependencies.py
```

### 3. System Preparation (Manual)
#### Update System Packages
Ensure your Raspberry Pi's system packages are up to date:
```bash
sudo apt update && sudo apt upgrade -y
```

#### Install Python & Pip
Check your current Python version:
```bash
python3 --version
```
Update Python if needed:
```bash
sudo apt install python3 -y
```
Ensure pip is installed and updated:
```bash
sudo apt install python3-pip -y
sudo python3 -m pip install --upgrade pip
```

---

### 4. Install Required Libraries
#### Install CustomTkinter
```bash
sudo apt install python3-tk -y
sudo pip3 install customtkinter --break-system-packages
```
#### Install Pygame
```bash
sudo pip3 install pygame --break-system-packages
```
```bash
sudo apt install python3-dev libsdl2-dev libsdl2-image-dev \
libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev \
libjpeg-dev -y
```

#### Install GPIO Library

`python3-rpi.gpio` allows Game Center to read input from physical buttons connected to the Raspberry Pi's GPIO pins.

```bash
sudo apt install python3-rpi.gpio -y
```

#### Install Keyboard Library
The `keyboard `  library is used to emulate key presses based on GPIO input, letting physical buttons control games as if you're using a keyboard.
```bash
sudo pip3 install keyboard --break-system-packages
```
#### Install mGBA-Qt Emulator (Game Boy Advance for External Games)
`mgba-qt` is a lightweight emulator used in Game Center to run external Game Boy Advance (GBA) games seamlessly within the console.
```bash
sudo apt install mgba-qt
```

#### Install xdotool (For Focus Mode on Startup)
`xdotool` is used to simulate key presses or mouse clicks. In Game Center, it ensures that the application window gains focus automatically upon startup.
```bash
sudo apt install xdotool -y
```

---

### 5. Set Up Auto-Launch on Startup
Create a systemd service to launch Game Center automatically:
```bash
sudo nano /etc/systemd/system/gamecenter.service
```
Paste the following configuration (replace `<USER>` with your Raspberry Pi username and `<PATH>` with the full path to the Game Center folder):
```
[Unit]
Description=Game Center GUI Application
After=multi-user.target

[Service]
User=<USER>
Group=<USER>
WorkingDirectory=<PATH>
ExecStart=/usr/bin/python3 <PATH>/main.py
Environment=DISPLAY=:0
Restart=always

[Install]
WantedBy=multi-user.target
```
Save the file and enable the service:
```bash
sudo systemctl enable gamecenter.service
sudo systemctl start gamecenter.service
```
Check service status:
```bash
sudo systemctl status gamecenter.service
```
Restart your Raspberry Pi to verify auto-launch:
```bash
sudo reboot
```

If you cloned the repository into a new directory, remember to update `<PATH>` in the service file accordingly.

---


---

### 6. Troubleshooting Common Issues
#### ImageTk Not Found (PIL Issue)
If you encounter an error related to ImageTk from PIL, try:
```bash
sudo apt install --reinstall python3-pil python3-tk
pip install --break-system-packages --upgrade --force-reinstall pillow
```

