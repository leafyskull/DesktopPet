import sys

from PySide6.QtCore import (
    Qt, QPoint,                                # For window flags
    QTimer                                     # For updating the pet's position and behavior
)
from PySide6.QtGui import QPixmap, QTransform  # For images/assets and transformations
from PySide6.QtWidgets import (
    QApplication,
    QWidget,                                   # For creating the application
    QLabel,                                    # For displaying the pet visuals
    )



"""
Class for the desktop pet.
This will handle appearance, movement, interactions, behavior, etc.
"""
class DesktopPet(QWidget):

    def __init__(self, name):
        """Initialize the desktop pet."""

        super().__init__()

        self.name = name

        self.is_dragging = False

        # Load sprite sheet for the pet
        self.sprite_sheet = QPixmap("assets/cat_spritesheet.png")
        if self.sprite_sheet.isNull():
            print("Error: Could not load sprite sheet.")
            sys.exit(1)

        # The current art I'm using is 32x32.
        self.frame_width = 32
        self.frame_height = 32
        self.resize(self.frame_width, self.frame_height)

        # Placeholder frame from the sprite sheet
        # TODO: Animations
        row = 4
        column = 0
        x = column * self.frame_width
        y = row * self.frame_height
        frame = self.sprite_sheet.copy(x, y, self.frame_width, self.frame_height)

        scale = 3
        frame = frame.scaled(
            self.frame_width * scale,
            self.frame_height * scale,
            Qt.KeepAspectRatio,
            Qt.FastTransformation
        )

        # Make the window the same size as the image
        self.resize(self.frame_width * scale, self.frame_height * scale)

        self.pet_label = QLabel(self)
        self.pet_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.pet_label.setPixmap(frame)

        # Keep the pet on top of other windows
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        # Set the background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Default position
        self.move(100, 100)

        # Movement settings
        self.speed = 2
        self.direction = 1 # | 1 = Right | -1 = Left |

        # Update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pet)
        self.timer.start(30)  # Update every 30 ms


    def update_pet(self):
        """Update the pet's position and behavior."""

        if self.is_dragging: return  # Don't move if the pet is being dragged

        # So pet can't walk off screen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Update position
        new_x = self.x() + (self.speed * self.direction)

        # If we hit the left side, go right
        if new_x <= screen_geometry.left():
            new_x = screen_geometry.left()
            self.direction *= -1

        # If we hit the right side, go left
        elif new_x + self.width() >= screen_geometry.right():
            new_x = screen_geometry.right() - self.width()
            self.direction *= -1

        self.move(new_x, self.y())


    def mousePressEvent(self, event):
        """Handle mouse press events for picking up the pet."""

        if event.button() == Qt.LeftButton:
            self.is_dragging = True
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


    def mouseReleaseEvent(self, event):
        """Handle mouse release events for dropping the pet."""
        if event.button() == Qt.LeftButton:
            self.is_dragging = False


