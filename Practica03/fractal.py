from constantes import DEBUG, DEFAULT_FRACTAL_ITER
from linea import Linea
from poligono import Poligono
from punto import Punto


class Fractal(Poligono):
    def __init__(self, type, startX, startY, endX, endY, algoritmo, color):
        self.type = type
        super(Fractal, self).__init__()
        self.generatelines(startX, startY, endX, endY, algoritmo, color)

    def generatelines(self, startX, startY, endX, endY, algoritmo, color):

        switch = {
            0: self.createsierpinsky,
        }

        if DEBUG: print('Creando fractal: ' + str(self.type))

        switch[self.type](startX, startY, endX, endY, algoritmo, color)

    def createsierpinsky(self, startX, startY, endX, endY, algoritmo, color):
        punto1 = Punto(startX, startY)
        punto2 = Punto((startX + endX) // 2, endY)
        punto3 = Punto(endX, startY)

        self.createsierpinskyrec(punto1, punto2, punto3, algoritmo, color, DEFAULT_FRACTAL_ITER)

    def createsierpinskyrec(self, p1, p2, p3, algoritmo, color, n):

        if n == 0:
            self.addlinea(Linea(p1, p2, algoritmo, color), None)
            self.addlinea(Linea(p2, p3, algoritmo, color), None)
            self.addlinea(Linea(p3, p1, algoritmo, color), None)
        else:
            new1 = Punto((p1.getX() + (p2.getX() - p1.getX()) // 2), (p1.getY() + (p2.getY() - p1.getY()) // 2))
            new2 = Punto((p3.getX() + (p2.getX() - p3.getX()) // 2), (p3.getY() + (p2.getY() - p3.getY()) // 2))
            new3 = Punto((p1.getX() + (p3.getX() - p1.getX()) // 2), (p1.getY() + (p3.getY() - p1.getY()) // 2))

            n -= 1

            self.createsierpinskyrec(new1, p2, new2, algoritmo, color, n)
            self.createsierpinskyrec(p1, new1, new3, algoritmo, color, n)
            self.createsierpinskyrec(new3, new2, p3, algoritmo, color, n)