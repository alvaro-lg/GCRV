class Snapshot:

    def __init__(self, poligonos, puntosTmp, poligonoTmp, lineatarget, poligonotarget):
        self.poligonos = poligonos
        self.puntosTmp = puntosTmp
        self.poligonoTmp = poligonoTmp
        self.lineatarget = lineatarget
        self.poligonotarget = poligonotarget

    def getvalues(self):
        return self.poligonos, self.puntosTmp, self.poligonoTmp, self.lineatarget, self.poligonotarget