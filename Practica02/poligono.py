class Poligono:

    def __init__(self):
        self.lineas = dict()

    def addlinea(self, linea, puntos):
        self.lineas[linea] = puntos

    def removelinea(self, linea):
        del self.lineas[linea]

    def getlineas(self):
        return self.lineas

