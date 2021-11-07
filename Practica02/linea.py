class Linea:
    def __init__(self, punto1, punto2, algoritmo, color):
        self.start = punto1
        self.end = punto2
        self.algoritmo = algoritmo
        self.color = color

    def getstart(self):
        return self.start

    def setstart(self, start):
        self.start = start

    def getend(self):
        return self.end

    def setend(self, end):
        self.end = end

    def getalgoritmo(self):
        return self.algoritmo

    def setalgoritmo(self, algoritmo):
        self.algoritmo = algoritmo

    def getcolor(self):
        return self.color

    def setcolor(self, color):
        self.color = color

    def getcomplementaryColor(self):
        my_hex = self.getcolor()
        if my_hex[0] == '#':
            my_hex = my_hex[1:]
        rgb = (my_hex[0:2], my_hex[2:4], my_hex[4:6])
        comp = ['%02X' % (255 - int(a, 16)) for a in rgb]
        return '#' + ''.join(comp)
