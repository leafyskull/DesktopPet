from PySide6.QtCore import Qt
from pet_state import PetState


class Init_Animations:

    # This is used to choose the angle of the cat from the spritesheet.
    # 4 = front/side
    # 5 = side
    START_ROW = 5

    def initialize_all_animations(self, pet: DesktopPet):
        """Initializes all animations."""
        
        pet.walk_frames = self.init_frames_for_animation(self, pet, PetState.WALKING)
        pet.idle_frames = self.init_frames_for_animation(self, pet, PetState.IDLE)
        pet.react_frames = self.init_frames_for_animation(self, pet, PetState.REACTING)
        pet.laying_down_frames = self.init_frames_for_animation(self, pet, PetState.LAYING_DOWN)
        pet.running_frames = self.init_frames_for_animation(self, pet, PetState.RUNNING)

        
    def get_start_col_for_state(pet_state: PetState) -> int:
        """Returns the starting column in the spritesheet for a given pet"""
        pet_state_to_col_dict = {
            PetState.WALKING: 12,
            PetState.IDLE: 0,
            PetState.REACTING: 4,
            PetState.LAYING_DOWN: 8,
            PetState.RUNNING: 20
        }

        return pet_state_to_col_dict[pet_state]


    def get_num_frames_for_state(pet_state: PetState) -> int:
        """Returns the number of frames in an animation for a given state."""
        pet_state_to_num_frames_dict = {
            PetState.WALKING: 4,
            PetState.IDLE: 6,
            PetState.REACTING: 5,
            PetState.LAYING_DOWN: 8,
            PetState.RUNNING: 8
        }

        return pet_state_to_num_frames_dict[pet_state]


    def init_frames_for_animation(self, pet: DesktopPet, pet_state: PetState):
        """Initializes the frames for a given animation."""

        anim_start_row = self.START_ROW
        anim_start_col = self.get_start_col_for_state(pet_state)

        anim_frames = []

        NUM_ANIM_FRAMES = self.get_num_frames_for_state(pet_state)
        initialized_frame_count = 0

        for row in range(2):
            for col in range(4):
                x = (anim_start_col + col) * pet.frame_width
                y = (anim_start_row + row) * pet.frame_height
    
                frame = pet.sprite_sheet.copy(x, y, pet.frame_width, pet.frame_height)
    
                frame = frame.scaled(
                    pet.frame_width * pet.VISUAL_SCALE,
                    pet.frame_height * pet.VISUAL_SCALE,
                    Qt.KeepAspectRatio,
                    Qt.FastTransformation
                )
    
                anim_frames.append(frame)

                initialized_frame_count += 1
                
                if initialized_frame_count >= NUM_ANIM_FRAMES:
                    return anim_frames

        return anim_frames
