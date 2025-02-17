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

### Installing CustomTkinter

The following command is required to install CustomTkinter on Raspberry Pi:

```bash
sudo pip3 install customtkinter --break-system-packages
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

The Game Center is configured to automatically launch when your Raspberry Pi starts up. This provides a seamless gaming experience without requiring manual program execution.

### Verifying Auto-Launch

After installation, restart your Raspberry Pi to confirm that the Game Center appears automatically at system startup.

## Support

If you encounter any issues or need assistance, please open an issue in the repository.
