#!/bin/bash

echo "Installing Fake Neofetch requirements..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed! Please install Python 3.8 or higher."
    echo "You can install Python using your package manager:"
    echo "Ubuntu/Debian: sudo apt install python3"
    echo "Fedora: sudo dnf install python3"
    echo "Arch: sudo pacman -S python"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed! Please install pip."
    echo "You can install pip using your package manager:"
    echo "Ubuntu/Debian: sudo apt install python3-pip"
    echo "Fedora: sudo dnf install python3-pip"
    echo "Arch: sudo pacman -S python-pip"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo
echo "Installation complete!"
echo "To run the application, activate the virtual environment and run:"
echo "source venv/bin/activate"
echo "python src/main.py"
echo 