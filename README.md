# Game Center for Raspberry Pi

A customizable game center built with CustomTkinter, designed to launch automatically on Raspberry Pi startup.

## Features

- Modern and intuitive user interface
- Auto-launch capability on system startup
- Built using CustomTkinter for enhanced visual appeal
- Optimized for Raspberry Pi systems

## Installation

### Prerequisites

- Raspberry Pi running Raspberry Pi OS
- Python 3.x
- pip3 package manager


## Follow this document and install/update your system 

 ```
https://docs.google.com/document/d/1fp7zQU_905RLOjTTQ0ateuz39ZRla9nzsfx0JWYQ6ik/edit?tab=t.0
```

### Installing CustomTkinter

The following command is required to install CustomTkinter on Raspberry Pi:

```bash
sudo pip3 install customtkinter --break-system-packages
```

### Installing Keyboard

The following command is required to install Keyboard library on Raspberry Pi, This library help us to press buttons on the keyboard:

```bash
sudo pip3 install keyboard --break-system-packages
```

**Note:** Standard pip installation methods may not work correctly on Raspberry Pi OS. The `--break-system-packages` flag is necessary for proper installation.

### Troubleshooting Common Issues

#### ImageTk Not Found Error

If you encounter the `ImageTk not found (from PIL)` error after installing CustomTkinter, follow these steps in order:

1. Reinstall Python3 PIL and Tk packages:
```bash
sudo apt install --reinstall python3-pil python3-tk
```

2. Force reinstall Pillow package:
```bash
pip install --break-system-packages --upgrade --force-reinstall pillow
```

## Auto-Launch Setup

To configure the Game Center to start automatically on boot, you'll need to create a systemd service. Follow these steps:

1. Create a new service file:
```bash
sudo nano /etc/systemd/system/gamecenter.service
```

2. Add the following content to the file (replace `<USER>` and `<PATH>` with your values):
```ini
[Unit]
Description=Game Center GUI Application
After=multi-user.target

[Service]
User=<USER>
Group=<USER>
WorkingDirectory=<PATH>/GUI
ExecStart=/usr/bin/python3 <PATH>/GUI/main.py
Environment=DISPLAY=:0
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl enable gamecenter.service
sudo systemctl start gamecenter.service
```

4. Check the service status:
```bash
sudo systemctl status gamecenter.service
```

### Verifying Auto-Launch

After setting up the service, restart your Raspberry Pi to confirm that the Game Center appears automatically at system startup:
```bash
sudo reboot
```

## Support

If you encounter any issues or need assistance, please open an issue in the repository.
