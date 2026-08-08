from PySide6.QtCore import Qt, QPoint                      # For window flags
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
        # TODO: Implement sprite sheet stuff
        self.pet_label = QLabel(self)
        self.pet_label.setAttribute(Qt.WA_TransparentForMouseEvents)
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


    def mousePressEvent(self, event):
        """Handle mouse press events for picking up the pet."""

        if event.button() == Qt.LeftButton:
            self.drag_positon = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
        elif event.button() == Qt.RightButton:
            self.close()  # Close the pet on right click
                          # TODO: Implement a more graceful way to close.


    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging the pet."""
        if event.buttons() & Qt.LeftButton:
            self.move(
                event.globalPosition().toPoint() - self.drag_positon
            )


