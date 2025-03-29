from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QMainWindow,
                              QPushButton, QDialog, QColorDialog, QHBoxLayout, QLabel, QFrame,
                              QGraphicsDropShadowEffect, QMessageBox, QFileDialog)
from PyQt6.QtGui import QFont, QPalette, QColor, QTextCharFormat, QTextCursor, QIcon, QFontMetrics
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional, Dict

class TerminalWindow(QMainWindow):
    def __init__(self, content: str, theme: Dict[str, str], font_family: str, font_size: int):
        super().__init__()
        self.setWindowTitle("Terminal")
        self.setMinimumSize(800, 600)
        
        # Set window background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(theme["background"]))
        self.setPalette(palette)
        
        # Create central widget with margins
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        
        # Create titlebar
        titlebar = QWidget()
        titlebar.setFixedHeight(30)
        titlebar_layout = QHBoxLayout(titlebar)
        titlebar_layout.setContentsMargins(10, 0, 10, 0)
        
        # Window controls (circles)
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        control_layout.setSpacing(5)
        control_layout.setContentsMargins(0, 0, 0, 0)
        
        # Close button (red circle)
        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(12, 12)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5f56;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #bf4342;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        control_layout.addWidget(self.close_btn)
        
        # Minimize button (yellow circle)
        self.min_btn = QPushButton()
        self.min_btn.setFixedSize(12, 12)
        self.min_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffbd2e;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #bf8e23;
            }
        """)
        self.min_btn.clicked.connect(self.showMinimized)
        control_layout.addWidget(self.min_btn)
        
        # Maximize button (green circle)
        self.max_btn = QPushButton()
        self.max_btn.setFixedSize(12, 12)
        self.max_btn.setStyleSheet("""
            QPushButton {
                background-color: #27c93f;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1f9a2f;
            }
        """)
        self.max_btn.clicked.connect(self.toggle_maximize)
        control_layout.addWidget(self.max_btn)
        
        titlebar_layout.addWidget(control_widget)
        
        # Title
        title = QLabel("Terminal")
        title.setStyleSheet(f"""
            color: {theme["text"]};
            font-weight: bold;
            font-size: 12px;
        """)
        titlebar_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add spacer to match left side
        spacer = QWidget()
        spacer.setFixedWidth(50)
        titlebar_layout.addWidget(spacer)
        
        layout.addWidget(titlebar)
        
        # Add separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"""
            background-color: {theme["text"]};
            margin: 0 5px;
        """)
        layout.addWidget(separator)
        
        # Create terminal widget
        self.terminal = TerminalWidget(is_preview=False)
        self.terminal.set_theme_colors(theme)
        self.terminal.set_font_family(font_family)
        self.terminal.set_font_size(font_size)
        self.terminal.set_content(content)
        
        # Style the terminal widget
        self.terminal.setStyleSheet(f"""
            QWidget {{
                background-color: {theme["background"]};
                border: none;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {theme["background"]};
                width: 10px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255, 255, 255, 0.1);
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """)
        
        layout.addWidget(self.terminal)
        
        self.setCentralWidget(central_widget)
        
        # Set window flags for custom titlebar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Variables for window dragging
        self.dragging = False
        self.offset = None
        titlebar.mousePressEvent = self.titlebar_mouse_press
        titlebar.mouseMoveEvent = self.titlebar_mouse_move
        titlebar.mouseReleaseEvent = self.titlebar_mouse_release
        
        # Add window shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 100))
        central_widget.setGraphicsEffect(shadow)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def titlebar_mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def titlebar_mouse_move(self, event):
        if self.dragging and self.offset:
            new_pos = self.mapToGlobal(event.pos() - self.offset)
            # Ensure window stays within screen bounds
            screen = self.screen()
            if screen:
                screen_geom = screen.geometry()
                new_pos.setX(max(screen_geom.left(), min(new_pos.x(), screen_geom.right() - self.width())))
                new_pos.setY(max(screen_geom.top(), min(new_pos.y(), screen_geom.bottom() - self.height())))
            self.move(new_pos)

    def titlebar_mouse_release(self, event):
        self.dragging = False

class TerminalWidget(QWidget):
    themeChanged = pyqtSignal(dict)
    fontChanged = pyqtSignal(str, int)

    def __init__(self, is_preview: bool = False):
        super().__init__()
        try:
            self.is_preview = is_preview
            self.current_font_family = "Ubuntu Mono"
            self.current_font_size = 11
            self.current_logo = ""
            self.current_info = {}
            self.theme_colors = {
                "background": "#300A24",
                "text": "#FFFFFF",
                "user": "#E95420",
                "separator": "#E95420",
                "label": "#E95420",
                "info": "#FFFFFF",
                "logo": "#E95420"
            }
            self.init_ui()
            self.setup_styles()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize terminal widget: {str(e)}")
            raise

    def init_ui(self):
        try:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(0)
            
            # Create terminal container
            terminal_container = QFrame()
            terminal_container.setFrameShape(QFrame.Shape.NoFrame)
            terminal_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.theme_colors["background"]};
                    border-radius: 4px;
                }}
            """)
            
            container_layout = QVBoxLayout(terminal_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(0)
            
            # Create terminal display
            self.terminal = QTextEdit()
            self.terminal.setReadOnly(True)
            self.terminal.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
            self.terminal.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.terminal.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            
            # Calculate terminal size based on content
            metrics = QFontMetrics(QFont(self.current_font_family, self.current_font_size))
            char_width = metrics.horizontalAdvance('x')
            char_height = metrics.height()
            
            # Set size for approximately 80x24 characters
            self.terminal.setMinimumSize(char_width * 80 + 20, char_height * 24 + 20)
            
            # Set terminal style
            self.terminal.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {self.theme_colors["background"]};
                    color: {self.theme_colors["text"]};
                    border: none;
                    padding: 10px;
                    font-family: '{self.current_font_family}';
                    font-size: {self.current_font_size}pt;
                    line-height: 1.2;
                }}
                QScrollBar:vertical {{
                    border: none;
                    background: {self.theme_colors["background"]};
                    width: 8px;
                    margin: 0;
                }}
                QScrollBar::handle:vertical {{
                    background: rgba(255, 255, 255, 0.2);
                    min-height: 20px;
                    border-radius: 4px;
                }}
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                    border: none;
                    background: none;
                    height: 0;
                }}
            """)
            
            container_layout.addWidget(self.terminal)
            layout.addWidget(terminal_container)

            if self.is_preview:
                # Add "Open in Window" button for preview mode
                button_layout = QHBoxLayout()
                button_layout.setContentsMargins(0, 5, 0, 0)
                
                self.window_button = QPushButton("Open in Window")
                self.window_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.theme_colors["background"]};
                        color: {self.theme_colors["text"]};
                        padding: 8px 16px;
                        border: 1px solid {self.theme_colors["text"]};
                        border-radius: 4px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: {self.theme_colors["text"]};
                        color: {self.theme_colors["background"]};
                    }}
                """)
                self.window_button.clicked.connect(self.open_in_window)
                
                button_layout.addStretch()
                button_layout.addWidget(self.window_button)
                layout.addLayout(button_layout)

            # Set default styling
            self.apply_theme()
            self.update_font()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize terminal UI: {str(e)}")
            raise

    def setup_styles(self):
        """Setup text styles for different elements"""
        self.styles = {
            "user": self._create_format(self.theme_colors["user"]),
            "separator": self._create_format(self.theme_colors["separator"]),
            "label": self._create_format(self.theme_colors["label"]),
            "info": self._create_format(self.theme_colors["info"]),
            "logo": self._create_format(self.theme_colors["logo"]),
        }

    def _create_format(self, color: str) -> QTextCharFormat:
        """Create a text format with specified color"""
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        return format

    def apply_theme(self):
        """Apply the current theme colors"""
        palette = self.terminal.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(self.theme_colors["background"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(self.theme_colors["text"]))
        self.terminal.setPalette(palette)
        self.setup_styles()

    def update_font(self):
        """Update the terminal font"""
        font = QFont(self.current_font_family, self.current_font_size)
        self.terminal.setFont(font)
        self.update_content(self.current_logo, self.current_info)

    def set_theme_colors(self, colors: Dict[str, str]):
        """Set new theme colors"""
        self.theme_colors.update(colors)
        self.apply_theme()
        self.themeChanged.emit(self.theme_colors)

    def set_font_family(self, family: str):
        """Set the terminal font family"""
        self.current_font_family = family
        self.update_font()
        self.fontChanged.emit(self.current_font_family, self.current_font_size)

    def set_font_size(self, size: int):
        """Set the terminal font size"""
        self.current_font_size = size
        self.update_font()
        self.fontChanged.emit(self.current_font_family, self.current_font_size)

    def set_content(self, content: str):
        """Set raw content for the terminal"""
        self.terminal.setPlainText(content)

    def update_content(self, logo: str, info: Dict[str, str]):
        """Update the terminal content with new logo and system info"""
        try:
            self.current_logo = logo
            self.current_info = info
            
            # Clear existing content
            self.clear()
            
            cursor = self.terminal.textCursor()
            
            # Add logo with proper formatting
            if logo:
                cursor.insertText(logo + "\n", self.styles["logo"])
            
            # Add system info
            if info:
                # Calculate max label length for alignment
                info_lines = [(f"{k}:", v) for k, v in info.items()]
                if info_lines:
                    max_label_length = max(len(label) for label, _ in info_lines if label)
                    
                    # Add info lines with proper alignment and colors
                    for label, value in info_lines:
                        if label:
                            padding = " " * (max_label_length - len(label))
                            cursor.insertText(f"{label}{padding} ", self.styles["label"])
                            cursor.insertText(f"{value}\n", self.styles["info"])
            
            # Ensure content is visible
            self.terminal.setTextCursor(cursor)
            self.terminal.ensureCursorVisible()
            
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to update terminal content: {str(e)}")

    def open_in_window(self):
        """Open the current terminal content in a new window"""
        content = self.terminal.toPlainText()
        window = TerminalWindow(
            content,
            self.theme_colors,
            self.current_font_family,
            self.current_font_size
        )
        window.show()

    def copy_to_clipboard(self):
        """Copy terminal content to clipboard"""
        self.terminal.selectAll()
        self.terminal.copy()
        self.terminal.textCursor().clearSelection()

    def get_content(self) -> str:
        """Get the current terminal content as plain text"""
        return self.terminal.toPlainText()

    def append(self, text: str):
        """Append text to the terminal"""
        self.terminal.append(text)

    def clear(self):
        """Clear the terminal content"""
        self.terminal.clear()

    def take_screenshot(self):
        """Take a screenshot of the terminal content"""
        try:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save Screenshot",
                "",
                "PNG Files (*.png);;All Files (*)"
            )
            if file_name:
                # If no extension is provided, add .png
                if not file_name.lower().endswith('.png'):
                    file_name += '.png'
                
                # Take the screenshot
                pixmap = self.terminal.grab()
                pixmap.save(file_name)
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"Screenshot saved successfully to {file_name}"
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to save screenshot: {str(e)}"
            ) 