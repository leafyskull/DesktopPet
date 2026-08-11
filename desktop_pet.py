import sys                         # For PetState
import random                                  # For randomly selecting states
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
from init_animations import Init_Animations
from pet_state import PetState

"""
Class for the desktop pet.
This will handle appearance, movement, interactions, behavior, etc.
"""
class DesktopPet(QWidget):

    def __init__(self, name):
        """Initialize the desktop pet."""

        #### ANIMATION FRAMES ####
        self.walk_frames = []
        self.idle_frames = []
        self.react_frames = []
        self.laying_down_frames = []
        self.running_frames = []

        super().__init__()
        self.name = name

        self.is_dragging = False
        self.drag_start_position = 0

        self.change_state(PetState.IDLE) # Default starting state

        # Movement settings
        self.speed = 2
        self.direction = -1 # | 1 = Right | -1 = Left |

        # Load sprite sheet for the pet
        self.sprite_sheet = QPixmap("assets/cat_spritesheet.png")
        if self.sprite_sheet.isNull():
            print("Error: Could not load sprite sheet.")
            sys.exit(1)

        self.frame_width = 32
        self.frame_height = 32

        self.VISUAL_SCALE = 3

        # self.initialize_all_animations()
        animationInitializer = Init_Animations
        animationInitializer.initialize_all_animations(animationInitializer, self)

        self.current_frame = 0

        self.pet_label = QLabel(self)
        self.display_frame(self.idle_frames[self.current_frame])
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
        #self.move(100, 100)
        self.calculate_spawn_position_and_spawn_there()

        # Movement timer
        self.movement_timer = QTimer(self)
        self.movement_timer.timeout.connect(self.update_pet)
        self.movement_timer.start(30)

        # Animation timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(150)


    def calculate_spawn_position_and_spawn_there(self):
        #self.move(100, 100)

        screen = QApplication.primaryScreen()
        available = screen.availableGeometry()

        x = 100
        y = available.bottom() - self.height() + 24

        self.move(x, y)


    def update_pet(self):
        """Update the pet's state and position."""

        if self.is_dragging: return

        self.state_timer += 1

        #### WALKING STATE ####
        if self.state == PetState.WALKING:
            self.update_walking()

            # After about 5 seconds, stop walking
            if self.state_timer >= 200:
                nextAction = random.randint(0, 1) # | 0 = SITTING_DOWN | 1 = GETTING_DOWN_TO_LAY_DOWN

                if nextAction == 0: self.change_state(PetState.SITTING_DOWN)
                if nextAction == 1: self.change_state(PetState.GETTING_DOWN_TO_LAY_DOWN)

        #### RUNNING STATE ####
        elif self.state == PetState.RUNNING:
            self.update_running()

            # After about 5 seconds, stop running
            if self.state_timer >= 200:
                nextAction = random.randint(0, 1)

                if nextAction == 0: self.change_state(PetState.SITTING_DOWN)
                if nextAction == 1: self.change_state(PetState.GETTING_DOWN_TO_LAY_DOWN)

        #### IDLE STATE ####
        elif self.state == PetState.IDLE:
            # Stay still for around 2 seconds
            if self.state_timer >= 67:
                self.change_state(PetState.STANDING_UP)

        #### LAYING DOWN STATE ####
        elif self.state == PetState.LAYING_DOWN:
            # Lay down for around 5 seconds, then get up
            if self.state_timer >= 167:
                self.change_state(PetState.GETTING_UP_FROM_LAYING_DOWN)


    def update_animation(self):
        """Updates the current animation's frames."""

        #### WALKING ####
        if self.state == PetState.WALKING:
            self.current_frame += 1

            if self.current_frame >= len(self.walk_frames):
                self.current_frame = 0

            self.display_frame(self.walk_frames[self.current_frame])

        #### RUNNING ####
        elif self.state == PetState.RUNNING:
            self.current_frame += 1

            if self.current_frame >= len(self.running_frames):
                self.current_frame = 0

            self.display_frame(self.running_frames[self.current_frame])

        #### SITTING DOWN ####
        elif self.state == PetState.SITTING_DOWN:
            self.display_frame(self.idle_frames[self.current_frame])

            self.current_frame += 1

            if self.current_frame >= len(self.idle_frames):
                self.change_state(PetState.IDLE)

        #### IDLE ####
        elif self.state == PetState.IDLE:
            self.display_frame(self.idle_frames[-1])

        #### STANDING UP ####
        elif self.state == PetState.STANDING_UP:
            self.display_frame(self.idle_frames[self.current_frame])

            self.current_frame -= 1

            if self.current_frame < 0:
                randomValue = random.randint(0, 1)
                if randomValue == 0: self.change_state(PetState.WALKING) 
                elif randomValue == 1: self.change_state(PetState.RUNNING)

        #### REACTING ####
        elif self.state == PetState.REACTING:
            self.display_frame(self.react_frames[self.current_frame])

            self.current_frame += 1

            if self.current_frame >= len(self.react_frames):
                self.change_state(PetState.IDLE)

        #### GETTING DOWN TO LAY DOWN ####
        elif self.state == PetState.GETTING_DOWN_TO_LAY_DOWN:
            self.display_frame(self.laying_down_frames[self.current_frame])

            self.current_frame += 1

            if self.current_frame >= len(self.laying_down_frames):
                self.change_state(PetState.LAYING_DOWN)

        #### LAYING DOWN ####
        elif self.state == PetState.LAYING_DOWN:
            self.display_frame(self.laying_down_frames[-1])

        #### GETTING UP FROM LAYING DOWN ####
        elif self.state == PetState.GETTING_UP_FROM_LAYING_DOWN:
            self.display_frame(self.laying_down_frames[self.current_frame])

            self.current_frame -= 1

            if self.current_frame < 0:
                randomValue = random.randint(0, 1)
                if randomValue == 0: self.change_state(PetState.WALKING) 
                elif randomValue == 1: self.change_state(PetState.RUNNING)


    def update_walking(self):
        """Update the walking animation."""

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

    def update_running(self):
        """Update the running animation."""
        
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Update position
        new_x = self.x() + (self.speed * 2 * self.direction)

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
        """Resets the state timer and changes state."""

        self.state = new_state
        self.state_timer = 0

        if new_state == PetState.WALKING or new_state == PetState.RUNNING:
            self.current_frame = 0

            # Walk/run for around 2-6 seconds
            self.state_duration = random.randint(70, 200)

            # Randomly choose left or right
            self.direction = random.choice([-1, 1])

        elif new_state == PetState.SITTING_DOWN:
            self.current_frame = 0

        elif new_state == PetState.STANDING_UP:
            self.current_frame = len(self.idle_frames) - 1

            # Sit for roughly 2-5 seconds
            self.state_duration = random.randint(70, 170)

        elif new_state == PetState.REACTING:
            self.current_frame = 0

        elif new_state == PetState.GETTING_DOWN_TO_LAY_DOWN:
            self.current_frame = 0

        elif new_state == PetState.GETTING_UP_FROM_LAYING_DOWN:
            self.current_frame = len(self.laying_down_frames) - 1

            # Lay down for roughly 2-5 seconds
            self.state_duration = random.randint(70, 170)


    def display_frame(self, frame):
        """Displays the requested frame, and sets the direction."""

        if self.direction == 1: # RIGHT
            frame = frame.transformed(QTransform().scale(-1, 1))
        elif self.direction == -1: # LEFT
            frame = frame.transformed(QTransform().scale(1, 1))

        self.pet_label.setPixmap(frame)



    #### **** MOUSE HANDLING **** ####

    def mousePressEvent(self, event):
        """Handle mouse press events for picking up the pet."""

        if event.button() == Qt.LeftButton:

            self.is_dragging = True

            self.drag_start_position = event.globalPosition().toPoint()

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

            release_position = event.globalPosition().toPoint()

            distance = (release_position - self.drag_start_position).manhattanLength()

            if distance < 5:
                self.change_state(PetState.REACTING)


