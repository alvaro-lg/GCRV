import numpy as np

from constantes import DEBUG, DEGREES_TO_RADIANS
from linea import Linea
from punto import Punto
from math import *

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

    def applyanimation(self, linea, time):

        if time <= self.startTime:
            return linea
        elif time > self.endTime:
            time = self.endTime

        switch = {
            0: self.applytranslation,
            1: self.applyscaling,
            2: self.applyrotation,
            3: self.applyshearing,
            4: self.applyhreflexion,
            5: self.applyvreflexion
        }

        if DEBUG: print('Aplicando animacion: ' + str(self.type))

        self.xTime = time
        newVecX = (self.vecX * time) / self.endTime
        newVecY = (self.vecY * time) / self.endTime

        return switch[self.type](linea, newVecX, newVecY)

    def applytranslation(self, linea, newVecX, newVecY):

        matrix = np.array([[1, 0, newVecX], [0, 1, newVecY], [0, 0, 1]])
        p1 = np.array([linea.getstart().getX(), linea.getstart().getY(), 1])
        p2 = np.array([linea.getend().getX(), linea.getend().getY(), 1])

        newStart = matrix @ p1.T
        newEnd = matrix @ p2.T

        return Linea(Punto(int(newStart[0]), int(newStart[1])), Punto(int(newEnd[0]), int(newEnd[1])), \
                     linea.getalgoritmo(), linea.getcolor())

    def applyscaling(self, linea, newVecX, newVecY):

        matrix = np.array([[newVecX, 0, 0], [0, newVecY, 0], [0, 0, 1]])
        p1 = np.array([linea.getstart().getX(), linea.getstart().getY(), 1])
        p2 = np.array([linea.getend().getX(), linea.getend().getY(), 1])

        newStart = matrix @ p1.T
        newEnd = matrix @ p2.T

        return Linea(Punto(int(newStart[0]), int(newStart[1])), Punto(int(newEnd[0]), int(newEnd[1])), \
                     linea.getalgoritmo(), linea.getcolor())

    def applyrotation(self, linea, newVecX, newVecY):

        vector_1 = [0, 1]
        vector_2 = [newVecX, newVecY]

        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        beta = np.arccos(dot_product) * DEGREES_TO_RADIANS
        alpha = (self.xTime * beta) / self.endTime

        matrix = np.array([[cos(alpha), -sin(alpha), 0], [sin(alpha), cos(alpha), 0], [0, 0, 1]])
        p1 = np.array([linea.getstart().getX(), linea.getstart().getY(), 1])
        p2 = np.array([linea.getend().getX(), linea.getend().getY(), 1])

        newStart = matrix @ p1.T
        newEnd = matrix @ p2.T

        return Linea(Punto(int(newStart[0]), int(newStart[1])), Punto(int(newEnd[0]), int(newEnd[1])), \
                     linea.getalgoritmo(), linea.getcolor())

    def applyshearing(self, linea, newVecX, newVecY):
        pass

    def applyhreflexion(self, linea, newVecX, newVecY):
        pass

    def applyvreflexion(self, linea, newVecX, newVecY):
        pass