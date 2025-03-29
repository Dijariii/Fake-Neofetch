from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QLabel, QSpinBox,
                             QCheckBox, QFileDialog, QMessageBox, QInputDialog,
                             QColorDialog, QFontComboBox, QFrame, QLineEdit,
                             QGroupBox, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
import os
from typing import Dict, Optional

from .terminal_widget import TerminalWidget
from ..hardware_info import SystemInfo
from ..ascii_art import AsciiArt
from ..profiles import ProfileManager

class SystemInfo:
    def __init__(self):
        self.os = "Ubuntu 22.04 LTS"
        self.host = "ubuntu-desktop"
        self.kernel = "5.15.0-91-generic"
        self.cpu = "Intel(R) Core(TM) i7-9700K"
        self.gpu = "NVIDIA GeForce RTX 3080"
        self.memory = "16GB / 32GB"
        self.uptime = "2 hours, 15 minutes"
        self.packages = "2345"
        self.shell = "bash 5.0.17"
        self.resolution = "1920x1080"
        self.de = "GNOME 42.5"
        self.wm = "Mutter"
        self.theme = "Adwaita [GTK3]"
        self.icons = "Adwaita [GTK3]"
        self.terminal = "gnome-terminal"
        self.cpu_usage = "25%"
        self.memory_usage = "4.2GB / 16GB"
        self.disk_usage = "234GB / 512GB"
        self.local_ip = "192.168.1.100"
        self.battery = "85%"

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'SystemInfo':
        info = cls()
        for k, v in data.items():
            if hasattr(info, k):
                setattr(info, k, v)
        return info

class MainWindow(QMainWindow):
    DISTRO_THEMES = {
        "Ubuntu": {
            "background": "#300A24",
            "text": "#FFFFFF",
            "user": "#E95420",
            "separator": "#E95420",
            "label": "#E95420",
            "info": "#FFFFFF",
            "logo": "#E95420"
        },
        "Arch": {
            "background": "#1793D1",
            "text": "#FFFFFF",
            "user": "#1793D1",
            "separator": "#1793D1",
            "label": "#1793D1",
            "info": "#FFFFFF",
            "logo": "#1793D1"
        },
        "Debian": {
            "background": "#A80030",
            "text": "#FFFFFF",
            "user": "#A80030",
            "separator": "#A80030",
            "label": "#A80030",
            "info": "#FFFFFF",
            "logo": "#A80030"
        },
        "Fedora": {
            "background": "#0F1C8C",
            "text": "#FFFFFF",
            "user": "#0F1C8C",
            "separator": "#0F1C8C",
            "label": "#0F1C8C",
            "info": "#FFFFFF",
            "logo": "#0F1C8C"
        },
        "Manjaro": {
            "background": "#35BF5C",
            "text": "#FFFFFF",
            "user": "#35BF5C",
            "separator": "#35BF5C",
            "label": "#35BF5C",
            "info": "#FFFFFF",
            "logo": "#35BF5C"
        },
        "Void": {
            "background": "#8A4D76",
            "text": "#FFFFFF",
            "user": "#8A4D76",
            "separator": "#8A4D76",
            "label": "#8A4D76",
            "info": "#FFFFFF",
            "logo": "#8A4D76"
        },
        "Gentoo": {
            "background": "#54487A",
            "text": "#FFFFFF",
            "user": "#54487A",
            "separator": "#54487A",
            "label": "#54487A",
            "info": "#FFFFFF",
            "logo": "#54487A"
        },
        "Kali": {
            "background": "#000000",
            "text": "#FFFFFF",
            "user": "#557C94",
            "separator": "#557C94",
            "label": "#557C94",
            "info": "#FFFFFF",
            "logo": "#557C94"
        },
        "Elementary": {
            "background": "#2D2D2D",
            "text": "#FFFFFF",
            "user": "#7B1E3D",
            "separator": "#7B1E3D",
            "label": "#7B1E3D",
            "info": "#FFFFFF",
            "logo": "#7B1E3D"
        },
        "Pop!_OS": {
            "background": "#000000",
            "text": "#FFFFFF",
            "user": "#48B9C7",
            "separator": "#48B9C7",
            "label": "#48B9C7",
            "info": "#FFFFFF",
            "logo": "#48B9C7"
        }
    }

    def __init__(self):
        super().__init__()
        try:
            self.setWindowTitle("Fake Neofetch")
            self.setMinimumSize(1200, 800)
            
            # Initialize components
            self.system_info = SystemInfo()
            self.ascii_art = AsciiArt()
            self.profile_manager = ProfileManager()
            
            # Create central widget and main layout
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QHBoxLayout(central_widget)
            main_layout.setContentsMargins(20, 20, 20, 20)
            main_layout.setSpacing(20)
            
            # Create left panel (controls)
            left_panel = QWidget()
            left_panel.setFixedWidth(300)  # Fixed width for better alignment
            left_layout = QVBoxLayout(left_panel)
            left_layout.setContentsMargins(0, 0, 0, 0)
            left_layout.setSpacing(15)  # Increased spacing between groups
            
            # Create scroll area for controls
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll.setStyleSheet("""
                QScrollArea {
                    background: transparent;
                    border: none;
                }
                QScrollArea > QWidget > QWidget {
                    background: transparent;
                }
            """)
            
            # Create container for controls
            controls_container = QWidget()
            controls_container.setObjectName("controls_container")
            controls_layout = QVBoxLayout(controls_container)
            controls_layout.setContentsMargins(0, 0, 0, 0)
            controls_layout.setSpacing(15)
            
            # Add control groups
            # Distribution selection
            distro_group = QGroupBox("Distribution")
            distro_layout = QVBoxLayout(distro_group)
            self.distro_combo = QComboBox()
            self.distro_combo.addItems(self.ascii_art.get_available_distros())
            distro_layout.addWidget(self.distro_combo)
            controls_layout.addWidget(distro_group)
            
            # Font settings
            font_group = QGroupBox("Font Settings")
            font_layout = QVBoxLayout(font_group)
            
            # Font family
            font_layout.addWidget(QLabel("Font Family:"))
            self.font_combo = QFontComboBox()
            self.font_combo.setCurrentFont(QFont("Ubuntu Mono"))
            font_layout.addWidget(self.font_combo)
            
            # Font size
            font_layout.addWidget(QLabel("Font Size:"))
            self.font_size = QSpinBox()
            self.font_size.setRange(8, 24)
            self.font_size.setValue(11)
            font_layout.addWidget(self.font_size)
            
            controls_layout.addWidget(font_group)
            
            # System Information
            info_group = QGroupBox("System Information")
            info_layout = QVBoxLayout(info_group)
            
            # Create input fields for each system info item
            self.info_inputs = {}
            for key, value in self.system_info.to_dict().items():
                label = QLabel(key.capitalize() + ":")
                input_field = QLineEdit(value)
                input_field.textChanged.connect(lambda text, k=key: self.update_info(k, text))
                self.info_inputs[key] = input_field
                info_layout.addWidget(label)
                info_layout.addWidget(input_field)
            
            controls_layout.addWidget(info_group)
            
            # Export controls
            export_group = QGroupBox("Export")
            export_layout = QVBoxLayout(export_group)
            
            self.copy_btn = QPushButton("Copy to Clipboard")
            self.screenshot_btn = QPushButton("Take Screenshot")
            export_layout.addWidget(self.copy_btn)
            export_layout.addWidget(self.screenshot_btn)
            
            controls_layout.addWidget(export_group)
            
            # Add stretch at the bottom
            controls_layout.addStretch()
            
            # Set the container as the scroll area widget
            scroll.setWidget(controls_container)
            left_layout.addWidget(scroll)
            
            # Create right panel (terminal)
            right_panel = QWidget()
            right_layout = QVBoxLayout(right_panel)
            right_layout.setContentsMargins(0, 0, 0, 0)
            
            # Create terminal widget
            self.terminal = TerminalWidget(is_preview=True)
            right_layout.addWidget(self.terminal)
            
            # Add panels to main layout
            main_layout.addWidget(left_panel)
            main_layout.addWidget(right_panel, 1)
            
            # Setup connections
            self.setup_connections()
            
            # Initial display
            self.update_display()
            
            # Set window style
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #333333;
                    border-radius: 4px;
                    margin-top: 1em;
                    padding: 15px;
                    background-color: #252525;
                    color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                    background-color: #252525;
                    color: #ffffff;
                }
                QPushButton {
                    padding: 8px 16px;
                    border: 1px solid #333333;
                    border-radius: 4px;
                    background-color: #2d2d2d;
                    color: #ffffff;
                    font-size: 12px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #353535;
                    border-color: #444444;
                }
                QPushButton:pressed {
                    background-color: #404040;
                }
                QComboBox, QFontComboBox {
                    padding: 8px;
                    border: 1px solid #333333;
                    border-radius: 4px;
                    background-color: #2d2d2d;
                    color: #ffffff;
                    font-size: 12px;
                }
                QComboBox:hover, QFontComboBox:hover {
                    border-color: #444444;
                }
                QComboBox::drop-down, QFontComboBox::drop-down {
                    border: none;
                    padding-right: 10px;
                }
                QComboBox::down-arrow, QFontComboBox::down-arrow {
                    image: none;
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;
                    border-top: 5px solid #ffffff;
                    margin-right: 5px;
                }
                QSpinBox {
                    padding: 8px;
                    border: 1px solid #333333;
                    border-radius: 4px;
                    background-color: #2d2d2d;
                    color: #ffffff;
                    font-size: 12px;
                }
                QSpinBox:hover {
                    border-color: #444444;
                }
                QSpinBox::up-button, QSpinBox::down-button {
                    border: none;
                    background: #353535;
                    width: 20px;
                }
                QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                    background: #404040;
                }
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #333333;
                    border-radius: 4px;
                    background-color: #2d2d2d;
                    color: #ffffff;
                    font-size: 12px;
                }
                QLineEdit:hover {
                    border-color: #444444;
                }
                QLineEdit:focus {
                    border-color: #555555;
                }
                QLabel {
                    color: #ffffff;
                    font-size: 12px;
                    margin-bottom: 2px;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #2d2d2d;
                    width: 8px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #454545;
                    min-height: 20px;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #555555;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                    height: 0;
                }
            """)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize main window: {str(e)}")
            raise

    def update_display(self):
        """Update the terminal display with current settings"""
        distro = self.distro_combo.currentText()
        logo = self.ascii_art.get_logo(distro)
        self.terminal.update_content(logo, self.system_info.to_dict())

    def update_font(self):
        """Update the terminal font"""
        font_family = self.font_combo.currentFont().family()
        font_size = self.font_size.value()
        self.terminal.set_font_family(font_family)
        self.terminal.set_font_size(font_size)

    def update_theme(self, theme: Dict[str, str]):
        """Update the theme colors"""
        for color, button in self.color_buttons.items():
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme[color]};
                    border: 1px solid #666;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    border: 1px solid #999;
                }}
            """)

    def choose_color(self, color_type: str):
        """Open color dialog to choose a new color"""
        current_color = self.color_buttons[color_type].styleSheet().split("background-color: ")[1].split(";")[0]
        color = QColorDialog.getColor(QColor(current_color), self)
        if color.isValid():
            self.color_buttons[color_type].setStyleSheet(f"""
                QPushButton {{
                    background-color: {color.name()};
                    border: 1px solid #666;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    border: 1px solid #999;
                }}
            """)
            self.terminal.set_theme_colors({color_type: color.name()})

    def update_info(self, key: str, value: str):
        """Update system info and refresh display"""
        setattr(self.system_info, key, value)
        self.update_display()

    def create_profile(self):
        """Create a new profile"""
        name, ok = QInputDialog.getText(self, "New Profile", "Enter profile name:")
        if ok and name:
            self.profile_combo.addItem(name)
            self.profile_combo.setCurrentText(name)
            self.save_profile()

    def save_profile(self):
        """Save current settings as a profile"""
        name = self.profile_combo.currentText()
        if name:
            profile_data = {
                "name": name,
                "distro": self.distro_combo.currentText(),
                "font_family": self.font_combo.currentFont().family(),
                "font_size": self.font_size.value(),
                "theme": self.terminal.theme_colors,
                "system_info": self.system_info.to_dict()
            }
            self.profile_manager.save_profile(name, profile_data)

    def load_profile(self, name: str):
        """Load a saved profile"""
        if not name:
            return
            
        profile = self.profile_manager.load_profile(name)
        if profile:
            self.distro_combo.setCurrentText(profile["distro"])
            self.font_combo.setCurrentFont(QFont(profile["font_family"]))
            self.font_size.setValue(profile["font_size"])
            self.terminal.set_theme_colors(profile["theme"])
            for key, value in profile["system_info"].items():
                if key in self.info_inputs:
                    self.info_inputs[key].setText(value)
            self.update_display()

    def delete_profile(self):
        """Delete the current profile"""
        name = self.profile_combo.currentText()
        if name:
            self.profile_manager.delete_profile(name)
            self.profile_combo.removeItem(self.profile_combo.currentIndex())

    def setup_connections(self):
        """Set up connections for all widgets"""
        self.distro_combo.currentTextChanged.connect(self.update_display)
        self.font_combo.currentFontChanged.connect(self.update_font)
        self.font_size.valueChanged.connect(self.update_font)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.screenshot_btn.clicked.connect(self.take_screenshot)

    def copy_to_clipboard(self):
        """Copy the terminal content to the clipboard"""
        self.terminal.copy_to_clipboard()

    def take_screenshot(self):
        """Take a screenshot of the terminal"""
        self.terminal.take_screenshot() 