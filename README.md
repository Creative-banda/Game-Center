# Game Center for Raspberry Pi

A customizable game center built with CustomTkinter, designed to launch automatically on a Raspberry Pi. This application provides a full-screen, console-like experience for selecting and playing games.

![Logo](assets/logo.png)

## Features

- **Modern and Intuitive UI:** A sleek, dark-themed interface built with CustomTkinter.
- **Game and Screenshot Browser:** Easily switch between your game library and a gallery of your screenshots.
- **Auto-launch on Startup:** The Game Center launches automatically on boot, making your Raspberry Pi feel like a dedicated console.
- **Auto-update System:** Automatically pulls the latest updates from the git repository on startup.
- **GPIO Button Support:** Control the UI and games with physical buttons connected to the Raspberry Pi's GPIO pins.
- **Support for Python Games and Emulators:** Launch your own Pygame-based games or classic ROMs using the built-in mGBA emulator support.

## Getting Started

### Prerequisites

This project is designed to run on a Raspberry Pi, preferably a Raspberry Pi 4. You will need a fresh installation of Raspberry Pi OS.

### Installation

For detailed installation instructions, please see [INSTALL.md](INSTALL.md).

## Usage

Once installed, the Game Center will launch automatically on boot. Use the following GPIO-connected buttons (or the corresponding keyboard keys) to navigate the interface:

- **Up/Down (W/S):** Navigate through the game or screenshot list.
- **Left/Right (A/D):** Switch between the "Games" and "Screenshots" tabs.
- **Select (Space):** Launch the selected game.
- **Delete (F):** Delete the selected screenshot (a confirmation will appear).
- **Exit (Escape):** Hold for a few seconds to close the application.

## Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
