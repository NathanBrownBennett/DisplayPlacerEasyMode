# EasySetup.py

EasySetup.py is a Python script designed to simplify the process of managing and configuring display settings on macOS systems. It leverages the `displayplacer` command-line tool to provide a user-friendly interface for adjusting display resolutions, color depths, scaling options, rotation angles, and screen positioning.

## Features

- **List Displays**: Quickly view all connected displays and their current configurations.
- **Modify Display Settings**: Interactively change settings for each display, including resolution, color depth, scaling, rotation, and origin.
- **Generate and Apply Configuration**: Automatically generate `displayplacer` commands based on user modifications and apply them directly from the script.

## Prerequisites

Before using EasySetup.py, ensure you have the following installed on your macOS:

- **Python 3**: The script is written in Python 3.
- **Homebrew**: Used to install `displayplacer`.
- **DisplayPlacer**: A command-line utility for macOS to configure multiple displays. Install it via Homebrew with `brew install displayplacer`.

## Installation

1. Clone the repository or download the `EasySetup.py` script.
2. Ensure you have Python 3 installed on your system.
3. Install `displayplacer` using Homebrew:

## Usage

To use EasySetup.py, simply run the script from the terminal:
```
python EasySetup.py
```
Follow the on-screen prompts to list displays, modify settings, and apply your configurations.

## Contributing

Contributions to EasySetup.py are welcome! Please feel free to submit pull requests or open issues to suggest improvements or add new features.

## License

This project is open-source and available under the MIT License.