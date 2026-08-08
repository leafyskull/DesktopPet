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


        #### **** WALK ANIMATION **** ####

        self.frame_width = 32
        self.frame_height = 32

        self.walk_frames = []

        walk_start_row = 3
        walk_start_column = 12

        VISUAL_SCALE = 3

        for column in range(4):
            x = (walk_start_column + column) * self.frame_width
            y = walk_start_row * self.frame_height

            frame = self.sprite_sheet.copy(x, y, self.frame_width, self.frame_height)

            frame = frame.scaled(
                self.frame_width * VISUAL_SCALE,
                self.frame_height * VISUAL_SCALE,
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )

            self.walk_frames.append(frame)


        self.current_frame = 0

        self.pet_label = QLabel(self)
        self.pet_label.setPixmap(self.walk_frames[self.current_frame])
        self.resize(self.frame_width * VISUAL_SCALE, self.frame_height * VISUAL_SCALE)

        # Keep the pet on top of other windows
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        # Set background transparent, disable clicking transparent part.
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.pet_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Default starting position
        self.move(100, 100)

        # Movement settings
        self.speed = 2
        self.direction = -1 # | 1 = Right | -1 = Left |

        # Movement timer
        self.movement_timer = QTimer(self)
        self.movement_timer.timeout.connect(self.update_pet_position)
        self.movement_timer.start(30)

        # Animation timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(150)


    def update_pet_position(self):
        """Update the pet's position and behavior."""

        if self.is_dragging: return

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


    def update_animation(self):
        self.current_frame += 1

        if self.current_frame >= len(self.walk_frames):
            self.current_frame = 0

        self.pet_label.setPixmap(self.walk_frames[self.current_frame])


    def mousePressEvent(self, event):
        """Handle mouse press events for picking up the pet."""

        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_positon = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
        elif event.button() == Qt.RightButton:
            self.close()  # TODO: Implement a more graceful way to close.


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


