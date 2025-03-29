from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QLabel, QSpinBox,
                             QCheckBox, QFileDialog, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import os
from typing import Dict, Optional

from src.gui.terminal_widget import TerminalWidget
from src.hardware_info import SystemInfo
from src.ascii_art import AsciiArt
from src.profiles import ProfileManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fake Neofetch")
        self.setMinimumSize(800, 600)
        
        # Initialize components
        self.system_info = SystemInfo()
        self.ascii_art = AsciiArt()
        self.profile_manager = ProfileManager()
        
        self.init_ui()
        self.setup_connections()
        
        # Initial display
        self.update_display()

    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Create left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Profile controls
        profile_group = QWidget()
        profile_layout = QVBoxLayout(profile_group)
        
        # Profile selector
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(self.profile_manager.get_all_profiles())
        profile_layout.addWidget(QLabel("Profile:"))
        profile_layout.addWidget(self.profile_combo)
        
        # Profile buttons
        profile_buttons = QHBoxLayout()
        self.new_profile_btn = QPushButton("New Profile")
        self.save_profile_btn = QPushButton("Save Profile")
        self.delete_profile_btn = QPushButton("Delete Profile")
        profile_buttons.addWidget(self.new_profile_btn)
        profile_buttons.addWidget(self.save_profile_btn)
        profile_buttons.addWidget(self.delete_profile_btn)
        profile_layout.addLayout(profile_buttons)
        
        # Theme controls
        theme_group = QWidget()
        theme_layout = QVBoxLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        theme_layout.addWidget(QLabel("Theme:"))
        theme_layout.addWidget(self.theme_combo)
        
        # Font controls
        font_group = QWidget()
        font_layout = QVBoxLayout(font_group)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 20)
        self.font_size_spin.setValue(10)
        font_layout.addWidget(QLabel("Font Size:"))
        font_layout.addWidget(self.font_size_spin)
        
        # Distro controls
        distro_group = QWidget()
        distro_layout = QVBoxLayout(distro_group)
        
        self.distro_combo = QComboBox()
        self.distro_combo.addItems(self.ascii_art.get_available_distros())
        distro_layout.addWidget(QLabel("Distro:"))
        distro_layout.addWidget(self.distro_combo)
        
        # Export controls
        export_group = QWidget()
        export_layout = QVBoxLayout(export_group)
        
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.screenshot_btn = QPushButton("Take Screenshot")
        export_layout.addWidget(self.copy_btn)
        export_layout.addWidget(self.screenshot_btn)
        
        # Add all groups to left panel
        left_layout.addWidget(profile_group)
        left_layout.addWidget(theme_group)
        left_layout.addWidget(font_group)
        left_layout.addWidget(distro_group)
        left_layout.addWidget(export_group)
        left_layout.addStretch()
        
        # Create terminal display
        self.terminal = TerminalWidget()
        
        # Add widgets to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.terminal, 4)

    def setup_connections(self):
        # Profile connections
        self.profile_combo.currentTextChanged.connect(self.load_profile)
        self.new_profile_btn.clicked.connect(self.create_new_profile)
        self.save_profile_btn.clicked.connect(self.save_current_profile)
        self.delete_profile_btn.clicked.connect(self.delete_current_profile)
        
        # Theme connections
        self.theme_combo.currentTextChanged.connect(self.update_theme)
        
        # Font connections
        self.font_size_spin.valueChanged.connect(self.update_font_size)
        
        # Distro connections
        self.distro_combo.currentTextChanged.connect(self.update_display)
        
        # Export connections
        self.copy_btn.clicked.connect(self.terminal.copy_to_clipboard)
        self.screenshot_btn.clicked.connect(self.take_screenshot)

    def update_display(self):
        """Update the terminal display with current settings"""
        distro = self.distro_combo.currentText()
        logo = self.ascii_art.get_logo(distro)
        info = self.system_info.get_all()
        
        self.terminal.update_content(logo, info)

    def load_profile(self, name: str):
        """Load a saved profile"""
        if not name:
            return
            
        profile = self.profile_manager.get_profile(name)
        if profile:
            for key, value in profile.items():
                self.system_info.set_fake_info(key, value)
            self.update_display()

    def create_new_profile(self):
        """Create a new profile"""
        name, ok = QInputDialog.getText(self, "New Profile", "Enter profile name:")
        if ok and name:
            self.profile_manager.save_profile(name, self.system_info.get_all())
            self.profile_combo.addItem(name)
            self.profile_combo.setCurrentText(name)

    def save_current_profile(self):
        """Save the current profile"""
        name = self.profile_combo.currentText()
        if name:
            self.profile_manager.save_profile(name, self.system_info.get_all())
            QMessageBox.information(self, "Success", "Profile saved successfully!")

    def delete_current_profile(self):
        """Delete the current profile"""
        name = self.profile_combo.currentText()
        if name:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete profile '{name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.profile_manager.delete_profile(name)
                self.profile_combo.removeItem(self.profile_combo.currentIndex())

    def update_theme(self, theme: str):
        """Update the terminal theme"""
        self.terminal.set_theme(theme)

    def update_font_size(self, size: int):
        """Update the terminal font size"""
        self.terminal.set_font_size(size)

    def take_screenshot(self):
        """Take a screenshot of the terminal"""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", "", "PNG Files (*.png)"
        )
        if file_name:
            self.terminal.grab().save(file_name)
            QMessageBox.information(self, "Success", "Screenshot saved successfully!") 