from enum import Enum                          # For PetState
from PySide6.QtCore import Qt


class Init_Animations:

    def initialize_all_animations(self, pet: DesktopPet):
        """Initializes all animations."""

        self.init_walk_frames(self, pet)
        self.init_idle_frames(self, pet)
        self.init_reaction_frames(self, pet)
        self.init_laying_down_frames(self, pet)
        self.init_running_frames(self, pet)

    def init_walk_frames(self, pet: DesktopPet):
        """Initializes the frames for the walking animation."""

        walk_start_row = 3
        walk_start_column = 12

        for column in range(4):
            x = (walk_start_column + column) * pet.frame_width
            y = walk_start_row * pet.frame_height

            frame = pet.sprite_sheet.copy(x, y, pet.frame_width, pet.frame_height)

            frame = frame.scaled(
                pet.frame_width * pet.VISUAL_SCALE,
                pet.frame_height * pet.VISUAL_SCALE,
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )

            pet.walk_frames.append(frame)

    def init_idle_frames(self, pet: DesktopPet):
        """Initializes the frames for the idle animation."""

        idle_start_row = 3
        idle_start_column = 0

        NUM_IDLE_FRAMES = 6
        initialized_frame_count = 0

        for row in range(2):
            for column in range(4):
                x = (idle_start_column + column) * pet.frame_width
                y = (idle_start_row + row) * pet.frame_height

                frame = pet.sprite_sheet.copy(x, y, pet.frame_width, pet.frame_height)

                frame = frame.scaled(
                    pet.frame_width * pet.VISUAL_SCALE,
                    pet.frame_height * pet.VISUAL_SCALE,
                    Qt.KeepAspectRatio,
                    Qt.FastTransformation
                )

                pet.idle_frames.append(frame)

                initialized_frame_count += 1

                if initialized_frame_count >= NUM_IDLE_FRAMES:
                    return

    def init_reaction_frames(self, pet: DesktopPet):
        """Initializes the frames for the reacting state"""

        react_start_row = 3
        react_start_column = 4

        NUM_REACT_FRAMES = 5
        initialized_frame_count = 0

        for row in range(2):
            for column in range(4):
                x = (react_start_column + column) * pet.frame_width
                y = (react_start_row + row) * pet.frame_height

                frame = pet.sprite_sheet.copy(x, y, pet.frame_width, pet.frame_height)

                frame = frame.scaled(
                    pet.frame_width * pet.VISUAL_SCALE,
                    pet.frame_height * pet.VISUAL_SCALE,
                    Qt.KeepAspectRatio,
                    Qt.FastTransformation
                )

                pet.react_frames.append(frame)

                initialized_frame_count += 1

                if initialized_frame_count >= NUM_REACT_FRAMES:
                    return

    def init_laying_down_frames(self, pet: DesktopPet):
        """Initializes the frames for the laying down animation"""

        laying_down_start_row = 3
        laying_down_start_column = 8

        NUM_LAYING_DOWN_FRAMES = 8
        initialized_frame_count = 0

        for row in range(2):
            for column in range(4):
                x = (laying_down_start_column + column) * pet.frame_width
                y = (laying_down_start_row + row) * pet.frame_height

                frame = pet.sprite_sheet.copy(x, y, pet.frame_width, pet.frame_height)

                frame = frame.scaled(
                    pet.frame_width * pet.VISUAL_SCALE,
                    pet.frame_height * pet.VISUAL_SCALE,
                    Qt.KeepAspectRatio,
                    Qt.FastTransformation
                )

                pet.laying_down_frames.append(frame)

                initialized_frame_count += 1

                if initialized_frame_count >= NUM_LAYING_DOWN_FRAMES:
                    return

    def init_running_frames(self, pet: DesktopPet):
        """Initializes the frames for the running animation"""

        running_start_row = 3
        running_start_column = 20

        NUM_RUNNING_FRAMES = 8
        initialized_frame_count = 0

        for row in range(2):
            for column in range(4):
                x = (running_start_column + column) * pet.frame_width
                y = (running_start_row + row) * pet.frame_height

                frame = pet.sprite_sheet.copy(x, y, pet.frame_width, pet.frame_height)

                frame = frame.scaled(
                    pet.frame_width * pet.VISUAL_SCALE,
                    pet.frame_height * pet.VISUAL_SCALE,
                    Qt.KeepAspectRatio,
                    Qt.FastTransformation
                )

                pet.running_frames.append(frame)

                initialized_frame_count += 1

                if initialized_frame_count >= NUM_RUNNING_FRAMES:
                    return 