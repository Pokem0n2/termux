# HKA - Hyperlink Keyboard App

A lightweight Windows desktop app featuring a 5x5 button grid for quick link access.

## Features

- 5x5 grid of customizable shortcut buttons
- Click the `+` button to set a name and URL link
- Click a configured button to open its link in your default browser
- Configuration saved to `hka-config.json` in the same directory as the exe
- Single-file exe, no installation required

## Build from Source

### Prerequisites

- Python 3.8+
- Windows OS (for building the exe)

### Install dependencies

```bash
pip install auto-py-to-exe
```

### Build

```bash
auto-py-to-exe
```

Select:
- **Onefile**: One File
- **Windowed**: Window Based (hide console)

Or run via command line:

```bash
auto-py-to-exe --onefile --windowed --outputfilename HKA.exe main.py
```

### Manual Build with PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name HKA main.py
```

The exe will be in the `dist/` folder.

## Configuration

The app saves button configurations to `hka-config.json` next to the exe:

```json
{
  "0": {"name": "Google", "link": "https://google.com"},
  "5": {"name": "GitHub", "link": "https://github.com"}
}
```

Buttons are indexed 0-24 (left to right, top to bottom). You can edit this file manually.

## License

MIT
