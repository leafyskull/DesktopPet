from PySide6.QtCore import Qt                               # For window flags
from PySide6.QtGui import QPixmap                           # For loading images/assets
from PySide6.QtWidgets import QApplication, QWidget, QLabel # For creating the application



"""
Class for the desktop pet.
This will handle appearance, movement, interactions, behavior, etc.
"""
class DesktopPet(QWidget):

    def __init__(self, name):
        """Initialize the desktop pet."""

        super().__init__()

        self.name = name

        # Load pet image
        self.pet_label = QLabel(self)
        pixmap = QPixmap("assets/cat_spritesheet.png")
        self.pet_label.setPixmap(pixmap)

        # Keep the pet on top of other windows
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        # Set the background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Make the window the same size as the image
        self.resize(pixmap.size())

        # Default position
        self.move(100, 100)





