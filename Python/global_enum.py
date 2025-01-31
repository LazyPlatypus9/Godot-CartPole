from enum import Enum

class MessageTypeEnum(Enum):
    TERMINATION = 0
    PING = 1
    DATA = 2
    COMMAND = 3
    FEEDBACK = 4
    READY = 5

class InputsEnum(Enum):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    MOVE_UP = 2
    MOVE_DOWN = 3