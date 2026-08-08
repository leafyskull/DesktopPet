import sys
from enum import Enum

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


class PetState(Enum):
    """Represents the states the pet can be in."""
    WALKING = "walking"
    IDLE = "idle"
    SITTING_DOWN = "sitting_down"
    STANDING_UP = "standing_up"


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

        self.state = PetState.IDLE
        self.state_timer = 0

        # Load sprite sheet for the pet
        self.sprite_sheet = QPixmap("assets/cat_spritesheet.png")
        if self.sprite_sheet.isNull():
            print("Error: Could not load sprite sheet.")
            sys.exit(1)

        self.frame_width = 32
        self.frame_height = 32

        self.VISUAL_SCALE = 3

        self.walk_frames = []
        self.idle_frames = []
        self.init_walk_frames()
        self.init_idle_frames()

        self.current_frame = 0

        self.pet_label = QLabel(self)
        self.pet_label.setPixmap(self.idle_frames[self.current_frame])
        self.resize(
            self.frame_width * self.VISUAL_SCALE, 
            self.frame_height * self.VISUAL_SCALE
        )

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
        self.movement_timer.timeout.connect(self.update_pet)
        self.movement_timer.start(30)

        # Animation timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(150)


    def init_walk_frames(self):

        walk_start_row = 3
        walk_start_column = 12

        for column in range(4):
            x = (walk_start_column + column) * self.frame_width
            y = walk_start_row * self.frame_height

            frame = self.sprite_sheet.copy(x, y, self.frame_width, self.frame_height)

            frame = frame.scaled(
                self.frame_width * self.VISUAL_SCALE,
                self.frame_height * self.VISUAL_SCALE,
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )

            self.walk_frames.append(frame)


    def init_idle_frames(self):

        idle_start_row = 3
        idle_start_column = 0

        for column in range(4):
            x = (idle_start_column + column) * self.frame_width
            y = idle_start_row * self.frame_height

            frame = self.sprite_sheet.copy(x, y, self.frame_width, self.frame_height)

            frame = frame.scaled(
                self.frame_width * self.VISUAL_SCALE,
                self.frame_height * self.VISUAL_SCALE,
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )

            self.idle_frames.append(frame)


    def update_pet(self):
        """Update the pet's position."""

        if self.is_dragging: return

        self.state_timer += 1

        #### WALKING STATE ####
        if self.state == PetState.WALKING:
            self.update_walking()

            # After about 5 seconds, stop walking
            if self.state_timer >= 167:
                self.change_state(PetState.SITTING_DOWN)

        #### IDLE STATE ####
        elif self.state == PetState.IDLE:
            # Stay still for around 2 seconds
            if self.state_timer >= 67:
                self.change_state(PetState.STANDING_UP)


    def update_animation(self):

        #### WALKING ####
        if self.state == PetState.WALKING:
            self.current_frame += 1

            if self.current_frame >= len(self.walk_frames):
                self.current_frame = 0

            self.pet_label.setPixmap(self.walk_frames[self.current_frame])

        #### SITTING DOWN ####
        elif self.state == PetState.SITTING_DOWN:
            self.pet_label.setPixmap(self.idle_frames[self.current_frame])

            self.current_frame += 1

            if self.current_frame >= len(self.idle_frames):
                self.change_state(PetState.IDLE)

        #### IDLE ####
        elif self.state == PetState.IDLE:
            self.pet_label.setPixmap(self.idle_frames[-1])

        #### STANDING UP ####
        elif self.state == PetState.STANDING_UP:
            self.pet_label.setPixmap(self.idle_frames[self.current_frame])

            self.current_frame -= 1

            if self.current_frame < 0:
                self.change_state(PetState.WALKING)



    def update_walking(self):

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

    def change_state(self, new_state):
        self.state = new_state
        self.state_timer = 0

        if new_state == PetState.STANDING_UP:
            self.current_frame = len(self.idle_frames) - 1
        else:
            self.current_frame = 0





    #### **** MOUSE HANDLING **** ####

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


