from enum import Enum



class PetState(Enum):
    """Represents the states the pet can be in."""

    WALKING = "walking"
    RUNNING = "running"

    IDLE = "idle"
    SITTING_DOWN = "sitting_down"  # Sitting down into idle
    STANDING_UP = "standing_up"    # Standing up from idle

    REACTING = "reacting"

    LAYING_DOWN = "laying_down"
    GETTING_DOWN_TO_LAY_DOWN = "getting_down_to_lay_down"
    GETTING_UP_FROM_LAYING_DOWN = "getting_up_from_laying_down"
