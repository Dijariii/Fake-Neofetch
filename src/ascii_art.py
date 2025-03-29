import os
from typing import List, Optional
import yaml

class AsciiArt:
    def __init__(self):
        self.logo_dir = os.path.join("resources", "ascii", "distro_logos")
        self.logos = {}
        self.load_logos()

    def load_logos(self):
        """Load all available distro logos"""
        for file_name in os.listdir(self.logo_dir):
            if file_name.endswith(".txt"):
                distro_name = os.path.splitext(file_name)[0]
                with open(os.path.join(self.logo_dir, file_name), "r") as f:
                    self.logos[distro_name] = f.read()

    def get_logo(self, distro: str) -> str:
        """Get ASCII art logo for a specific distro"""
        return self.logos.get(distro.lower(), "")

    def add_logo(self, distro_name: str, logo: str) -> None:
        """Add a new logo to the collection"""
        self.logos[distro_name.lower()] = logo
        self._save_logo(distro_name, logo)

    def _save_logo(self, distro_name: str, logo: str) -> None:
        """Save a logo to the resources directory"""
        logos_dir = os.path.join(os.path.dirname(__file__), "..", "resources", "ascii", "distro_logos")
        if not os.path.exists(logos_dir):
            os.makedirs(logos_dir)

        filename = os.path.join(logos_dir, f"{distro_name.lower()}.txt")
        with open(filename, "w") as f:
            f.write(logo)

    def get_available_distros(self) -> List[str]:
        """Get list of available distro logos"""
        return list(self.logos.keys())

    def format_logo(self, logo: str, color: str = "default") -> str:
        """Format the logo with ANSI color codes"""
        if color == "default":
            return logo

        # Basic ANSI color codes
        colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "reset": "\033[0m"
        }

        if color not in colors:
            return logo

        # Apply color to non-empty lines
        lines = logo.split("\n")
        colored_lines = []
        for line in lines:
            if line.strip():
                colored_lines.append(f"{colors[color]}{line}{colors['reset']}")
            else:
                colored_lines.append(line)

        return "\n".join(colored_lines)

    def get_logo_height(self, logo: str) -> int:
        """Get the height of a logo in lines"""
        return len(logo.split("\n"))

    def get_logo_width(self, logo: str) -> int:
        """Get the width of a logo in characters"""
        return max(len(line) for line in logo.split("\n")) 