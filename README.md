<div align="center">

# Easy Minecraft Server

**Desktop tool to set up Minecraft servers in minutes, with a dark-themed graphical interface.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2%2B-ff5f6d)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## What is it?

A tool that automates the tedious part of setting up a Minecraft server: picking a version, downloading the right jar, accepting the EULA and writing the launch scripts. Everything is driven from a single-page graphical interface, with live install logs and a progress bar for every step.

## Features

- **Multiple server types**: Vanilla, Fabric, Forge and Paper.
- **MCDReforged integration**: optionally wraps any server type with MCDReforged for plugins and console management.
- **Automatic Java check**: detects whether Java is installed and warns if the version is too old.
- **Cross-platform launch scripts**: generates both `start.bat` and `start.sh`.
- Recent projects list for quick access to servers you've already created.

## Requirements

- [Python](https://www.python.org/) 3.10 or higher
- [Java](https://www.java.com/en/download/) 21 or higher (required to run the generated server, not to run this tool)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/froyln/easy-mc-server.git
   cd easy-mc-server
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Starting the App

To boot up Easy Minecraft Server, simply run:
```bash
python main.py
```

## Usage

1. Launch the app and check that Java is detected.
2. Click **Create New Server** and pick a project name and destination folder.
3. Choose a server type: Vanilla, Fabric, Forge or Paper.
4. Select the Minecraft version (and loader/installer version, for Fabric).
5. Set the minimum and maximum RAM.
6. Confirm, and watch the install log until it finishes.
7. Run `start.bat` (Windows) or `start.sh` (Linux/macOS) inside the created folder to launch the server.

## Project Structure

```
core/                   Server creation logic, no UI code
  system_check.py       Java / OS detection
  downloader.py         HTTP downloads with progress reporting
  process_runner.py     Streams subprocess output (used by the Forge installer)
  mcdreforged_setup.py  Install/init MCDReforged, edit its config
  launch_scripts.py     Generates start.bat / start.sh
  project_manager.py    Orchestrates a full server creation request
  recent_projects.py    Persists recently created servers
  server_types/         One installer class per server type
gui/                    CustomTkinter dark-themed interface
  app.py                Main window
  theme.py              Color palette and fonts
  pages/                Home view and the New Server wizard
  widgets/               Reusable UI components (console, cards, step indicator)
main.py                 Entry point
```

## Dependencies

[customtkinter](https://github.com/TomSchimansky/CustomTkinter)
[requests](https://pypi.org/project/requests/)
[mcdreforged](https://mcdreforged.com/en)

## License

[MIT](LICENSE) © froyln
