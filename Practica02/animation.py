from enum import Enum

class Animation:

    def __init__(self, type, startTime, endTime, vecX, vecY):
        self.type = type
        self.startTime = startTime
        self.endTime = endTime
        self.vecX = vecX
        self.vecY = vecY

    def gettype(self):
        return self.type

    def getstart(self):
        return self.startTime

    def getend(self):
        return self.endTime

    def getkey(self):
        return str(self.getstart()) + str(self.getend()) + str(self.gettype())