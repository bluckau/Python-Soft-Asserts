from enum import Enum

class Actions(Enum):
    NOTHING = 0 #placeholder, or for disabled actions
    WARN = 1
    SOFT_FAIL = 2 #(default)
    HARD_FAIL = 3