# Game Center for Raspberry Pi

A customizable game center built with CustomTkinter, designed to launch automatically on Raspberry Pi startup.

## Features
- Modern and intuitive user interface
- Auto-launch capability on system startup
- Built using CustomTkinter for enhanced visual appeal
- Optimized for Raspberry Pi systems
- **Auto-update system** to keep the application up-to-date with the latest changes

---

## Installation Guide

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

### 2. System Preparation
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

### 3. Install Required Libraries
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
```bash
sudo apt install python3-rpi.gpio -y
```

#### Install Keyboard Library
```bash
sudo pip3 install keyboard --break-system-packages
```
#### Install mGBA-Qt Emulator (Game Boy Advance for External Games)
```bash
sudo apt install mgba-qt
```

#### Install xdotool (For Focus Mode on Startup)
```bash
sudo apt install xdotool -y
```

#### Install Socket Library
```bash
sudo pip3 install socket --break-system-packages
```

---

### 4. Set Up Auto-Launch on Startup
Create a systemd service to launch Game Center automatically:
```bash
sudo nano /etc/systemd/system/gamecenter.service
```
Paste the following configuration (replace `<USER>` and `<PATH>` accordingly):
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

---

### 5. Clone the GitHub Repository
#### Install Git
Before cloning the repository, install Git if it’s not already installed:
```bash
sudo apt install git -y
```

#### Why We Need Git
Git allows us to download and manage the latest version of Game Center directly from the repository. This ensures we always have access to the newest features, bug fixes, and improvements. By using Git, we can easily update our application without manually downloading files.

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

---

### 6. Troubleshooting Common Issues
#### ImageTk Not Found (PIL Issue)
If you encounter an error related to ImageTk from PIL, try:
```bash
sudo apt install --reinstall python3-pil python3-tk
pip install --break-system-packages --upgrade --force-reinstall pillow
```

#### If Installation Fails
Try cleaning the pip cache and reinstalling:
```bash
sudo pip3 cache purge
sudo pip3 install pygame --force-reinstall
sudo pip3 install customtkinter --force-reinstall
```

#### If Dependencies Are Missing
Ensure all required dependencies are installed:
```bash
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev \
libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev \
python3-setuptools python3-dev python3-tk -y
```

---

### 7. Quick Installation (All-in-One Command)
Run this single command to install everything in one go:
```bash
sudo apt update && sudo apt upgrade -y && \
sudo apt install python3 -y && sudo python3 -m pip install --upgrade pip && \
sudo apt install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev \
libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev -y && \
sudo pip3 install pygame --break-system-packages && \
sudo apt install python3-tk -y && sudo pip3 install customtkinter --break-system-packages && \
sudo apt install python3-rpi.gpio -y && sudo apt install xdotool -y && \
sudo apt install --reinstall python3-pil python3-tk -y && \
pip install --break-system-packages --upgrade --force-reinstall pillow && \
sudo pip3 install socket --break-system-packages
```

### 🔹 Final Verification
Run this command to check if all dependencies are installed successfully:
```bash
python3 -c "import pygame, customtkinter, RPi.GPIO, socket; print('All libraries installed successfully!')"
```

