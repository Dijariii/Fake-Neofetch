from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QFont, QPalette, QColor, QTextCharFormat, QTextCursor
from PyQt6.QtCore import Qt
from typing import Optional

class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_styles()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Create terminal display
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        # Set default styling
        self.set_theme("dark")
        
        # Use monospace font
        font = QFont("Monospace", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.terminal.setFont(font)
        
        layout.addWidget(self.terminal)
        self.setLayout(layout)

    def setup_styles(self):
        """Setup text styles for different elements"""
        self.styles = {
            "title": self._create_format("#00ff00"),  # Green
            "info": self._create_format("#ffffff"),   # White
            "label": self._create_format("#00ffff"),  # Cyan
            "logo": self._create_format("#00ff00"),   # Green
            "separator": self._create_format("#666666")  # Gray
        }

    def _create_format(self, color: str) -> QTextCharFormat:
        """Create a text format with specified color"""
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        return format

    def set_theme(self, theme: str):
        """Set the terminal theme (light/dark)"""
        palette = self.terminal.palette()
        if theme == "dark":
            palette.setColor(QPalette.ColorRole.Base, QColor("#282828"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#F8F8F2"))
        else:
            palette.setColor(QPalette.ColorRole.Base, QColor("#F8F8F2"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#282828"))
        self.terminal.setPalette(palette)

    def update_content(self, logo: str, info: dict, color_scheme: Optional[dict] = None):
        """Update terminal content with formatted neofetch output"""
        self.terminal.clear()
        cursor = self.terminal.textCursor()

        # Apply logo
        if logo:
            cursor.insertText(logo + "\n", self.styles["logo"])

        # Calculate spacing for alignment
        max_label_length = max(len(k) for k in info.keys())
        spacing = " " * (max_label_length + 2)

        # Insert system information
        for label, value in info.items():
            # Label
            cursor.insertText(f"{label}:{spacing[len(label):]}", self.styles["label"])
            # Value
            cursor.insertText(f"{value}\n", self.styles["info"])

    def copy_to_clipboard(self):
        """Copy terminal content to clipboard"""
        self.terminal.selectAll()
        self.terminal.copy()
        self.terminal.textCursor().clearSelection()

    def get_content(self) -> str:
        """Get the current terminal content as plain text"""
        return self.terminal.toPlainText()

    def set_font_size(self, size: int):
        """Set the terminal font size"""
        font = self.terminal.font()
        font.setPointSize(size)
        self.terminal.setFont(font)

    def set_font_family(self, family: str):
        """Set the terminal font family"""
        font = self.terminal.font()
        font.setFamily(family)
        self.terminal.setFont(font)

    def set_color_scheme(self, scheme: dict):
        """Update the color scheme for different elements"""
        for element, color in scheme.items():
            if element in self.styles:
                self.styles[element] = self._create_format(color)

    def clear(self):
        """Clear the terminal content"""
        self.terminal.clear() 