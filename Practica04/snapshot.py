class Snapshot:

    def __init__(self, poligonos, puntosTmp, poligonoTmp, lineatarget, poligonotarget, fractales):
        self.poligonos = poligonos
        self.puntosTmp = puntosTmp
        self.poligonoTmp = poligonoTmp
        self.lineatarget = lineatarget
        self.poligonotarget = poligonotarget
        self.fractales = fractales

    def getvalues(self):
        return self.poligonos, self.puntosTmp, self.poligonoTmp, self.lineatarget, self.poligonotarget, self.fractales