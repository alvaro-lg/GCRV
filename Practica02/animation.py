from enum import Enum

class Animation:

    def __init__(self, type, start, end):
        self.type = type
        self.start = start
        self.end = end

    def gettype(self):
        return self.type

    def getstart(self):
        return self.start

    def getend(self):
        return self.end

    def getkey(self):
        return str(self.getstart()) + str(self.getend()) + str(self.gettype())


class AnimationTypes(Enum):
    TRANSLATION = 1
    SCALING = 2
    ROTATION = 3
    SHEARING = 4
    H_REFLEXION = 5
    V_REFLEXION = 6
