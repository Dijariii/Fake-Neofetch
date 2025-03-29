# Fake Neofetch 🖥️

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.4.0%2B-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🖥️ Modern GUI tool for creating ✨ customizable system info with 🐧 Linux themes.

![App Screenshot](screenshots/main.png)

## ✨ Features

- 🎨 Modern dark theme interface
- 🖼️ Real-time preview of your Neofetch output
- 🔄 Live customization of system information
- 🎯 Multiple Linux distribution themes
- 💾 Profile saving and loading
- 📋 Easy copy to clipboard
- 📸 Screenshot functionality
- 🖋️ Custom font support

## 🚀 Supported Distributions

The following Linux distributions are supported with their official themes and ASCII art:

| Distribution | Theme Preview |
|-------------|---------------|
| Ubuntu      | ![Ubuntu](screenshots/ubuntu.png) |
| Arch Linux  | ![Arch](screenshots/arch.png) |
| Debian      | ![Debian](screenshots/debian.png) |
| Fedora      | ![Fedora](screenshots/fedora.png) |
| Manjaro     | ![Manjaro](screenshots/manjaro.png) |
| Void Linux  | ![Void](screenshots/void.png) |
| Gentoo      | ![Gentoo](screenshots/gentoo.png) |
| Kali Linux  | ![Kali](screenshots/kali.png) |
| Elementary  | ![Elementary](screenshots/elementary.png) |
| Pop!_OS     | ![Pop_OS](screenshots/pop_os.png) |

## 📥 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Fake-Neofetch.git
cd Fake-Neofetch
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

Run the application:
```bash
python main.py
```

### Customization Options:

1. **Distribution Selection**
   - Choose from various Linux distributions
   - Each distribution comes with its unique theme and ASCII art

2. **Font Settings**
   - Select any system font
   - Adjust font size (8-24pt)

3. **System Information**
   - Customize all system information fields
   - Real-time preview updates

4. **Export Options**
   - Copy to clipboard
   - Save screenshots

## 🖼️ Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)

### Theme Examples
![Theme Examples](screenshots/themes.png)

### Font Customization
![Font Settings](screenshots/font_settings.png)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the original [Neofetch](https://github.com/dylanaraps/neofetch)
- ASCII art sourced from various Linux distributions
- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)