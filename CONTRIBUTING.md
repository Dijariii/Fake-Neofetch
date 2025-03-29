# Contributing to Fake Neofetch

Thank you for your interest in contributing to Fake Neofetch! This document provides guidelines and instructions for contributing to the project.

## Features

- Create custom neofetch-like displays
- Support for multiple Linux distributions
- Customizable themes and colors
- Font customization
- Profile management
- Live preview
- Copy to clipboard functionality
- macOS-style window controls
- Draggable windows
- Window shadow effects

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Fake-Neofetch.git
cd Fake-Neofetch
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
Fake-Neofetch/
├── src/
│   ├── gui/
│   │   ├── main_window.py
│   │   └── terminal_widget.py
│   ├── ascii_art.py
│   └── profiles.py
├── resources/
│   ├── ascii/
│   │   └── distro_logos/
│   └── profiles/
├── main.py
├── requirements.txt
└── README.md
```

## Adding New Features

### Adding New Distributions

1. Create a new ASCII art file in `resources/ascii/distro_logos/` with the name `distro_name.txt`
2. Add the distribution name to the list in `src/gui/main_window.py`
3. Add a theme color in the `DISTRO_THEMES` dictionary

### Adding New Themes

1. Add new theme colors to the `DISTRO_THEMES` dictionary in `src/gui/main_window.py`
2. Update the theme selection UI if needed

### Adding New System Info Fields

1. Add new fields to the `SystemInfo` class in `src/gui/main_window.py`
2. Update the UI to include new fields
3. Update the terminal display formatting

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for classes and methods
- Keep functions focused and single-purpose
- Use meaningful variable names
- Comment complex logic

## Testing

Before submitting a pull request:

1. Test the new feature thoroughly
2. Ensure all existing features still work
3. Check for any UI inconsistencies
4. Verify the code runs on different platforms

## Submitting Changes

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Description of your changes"
```

3. Push your changes:
```bash
git push origin feature/your-feature-name
```

4. Create a pull request on GitHub

## License

By contributing to Fake Neofetch, you agree that your contributions will be licensed under the project's MIT License. 