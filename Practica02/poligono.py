class Poligono:

    def __init__(self):
        self.lineas = dict()
        self.animaciones = list()

    def addlinea(self, linea, puntos):
        self.lineas[linea] = puntos

    def removelinea(self, linea):
        del self.lineas[linea]

    def getlineas(self):
        return self.lineas

    def __repr__(self):
        return str(len(self.lineas)) + ' lineas en total: ' + str(self.lineas)

    def getanimaciones(self):
        return self.animaciones

    def addanimacion(self, animacion):
        self.animaciones.append(animacion)

    def removeanimmacion(self, animacion):
        self.animaciones.remove(animacion)

