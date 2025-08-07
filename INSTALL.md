# Installation Guide for Game Center on Raspberry Pi

This guide provides step-by-step instructions for setting up the Game Center on a Raspberry Pi.

## 1. Configure Raspberry Pi OS

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

## 2. Clone the GitHub Repository

#### Install Git
Before cloning the repository, install Git if it’s not already installed:
```bash
sudo apt install git -y
```

#### Clone the Repository
To download the latest version of Game Center, clone the repository using Git:
```bash
git clone <REPO_URL>
```
Navigate into the project directory:
```bash
cd <REPO_FOLDER>
```

---

## 3. Install Dependencies

### 🔧 Easy Installation Script (Automated)
To make the setup process easier, we've created an automated Python script that installs all required libraries and dependencies for Game Center. Instead of installing each package manually, simply run the script and let it handle everything for you. This ensures a smooth and hassle-free installation experience.

```bash
python3 install_dependencies.py
```

### 🧰 Manual Setup (Advanced Users)

If you prefer manual installation:

#### System Preparation
```bash
sudo apt update
sudo python3 -m pip install --upgrade pip
```

#### Install Required Libraries

- **Install Python & Pip**
  ```bash
  sudo apt install python3-pip -y
  sudo python3 -m pip install --upgrade pip
  ```

- **Install CustomTkinter**
  ```bash
  sudo apt install python3-tk -y
  sudo pip3 install customtkinter --break-system-packages
  ```

- **Install Pygame**
  ```bash
  sudo pip3 install pygame --break-system-packages
  sudo apt install python3-dev libsdl2-dev libsdl2-image-dev \
  libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev \
  libjpeg-dev -y
  ```

- **Install GPIO Library**
  ```bash
  sudo apt install python3-rpi.gpio -y
  ```

- **Install Keyboard Library**
  ```bash
  sudo pip3 install keyboard --break-system-packages
  ```

- **Install mGBA-Qt Emulator**
  ```bash
  sudo apt install mgba-qt -y
  ```

- **Install xdotool**
  ```bash
  sudo apt install xdotool -y
  ```

- **Install grim**
  ```bash
  sudo apt install grim -y
  ```

---

## 4. Font Installation (Orbitron)

Replace `<PATH>` with the absolute path to the Game Center repository.
```bash
cd <PATH>
sudo mkdir -p /usr/share/fonts/truetype/orbitron
sudo cp assets/fonts/Orbitron.ttf /usr/share/fonts/truetype/orbitron/
sudo fc-cache -f -v
```

---

## 5. Auto-Start on Boot (systemd Service)

This will automatically launch the Game Center on boot.

#### Create the service file:
```bash
sudo nano /etc/systemd/system/gamecenter.service
```

Paste and update the following (replace `<USER>` and `<PATH>`):
```ini
[Unit]
Description=Game Center GUI Application
After=multi-user.target

[Service]
User=<USER>
Group=<USER>
WorkingDirectory=<PATH>
ExecStart=/usr/bin/python3 <PATH>/src/main.py
Environment=DISPLAY=:0
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Enable and start the service:
```bash
sudo systemctl enable gamecenter.service
sudo systemctl start gamecenter.service
```

To check the status of the service:
```bash
sudo systemctl status gamecenter.service
```

---

## 6. Reboot

After setup, reboot to verify auto-launch:
```bash
sudo reboot
```

---

## 7. Troubleshooting

- **Pillow / ImageTk Errors**
  ```bash
  sudo apt install --reinstall python3-pil python3-tk
  pip3 install --break-system-packages --upgrade --force-reinstall pillow
  ```

- **Service not launching?**
  Check the logs:
  ```bash
  sudo systemctl status gamecenter.service
  ```

- **Verifying Installation**
  Check that key packages are available by running `python3` and typing:
  ```python
  import pygame, customtkinter, RPi.GPIO, keyboard
  ```

---

## 8. Updating

To update the Game Center later, navigate to the repository folder and run:
```bash
git pull
```
If you encounter permission issues while updating, you may need to reset local changes:
```bash
git reset --hard
```
