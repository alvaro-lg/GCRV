
class Punto:

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def __repr__(self):
        return '(x: ' + str(self.x) + ', y: ' + str(self.y) +')'