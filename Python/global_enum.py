from enum import Enum

class MessageTypeEnum(Enum):
    TERMINATION = 1
    CONFIRMATION = 2
    DATA = 3,
    COMMAND = 4

class InputsEnum(Enum):
    MOVE_LEFT = 1,
    MOVE_RIGHT = 2,
    MOVE_UP = 3,
    MOVE_DOWN = 4