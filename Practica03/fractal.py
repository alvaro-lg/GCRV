import math

from numba import prange
from constantes import DEBUG
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
            1: self.createkotch,
            2: self.createmandelbrot,
            3: self.createjulia
        }

        if DEBUG: print('Creando fractal: ' + str(self.type))

        switch[self.type](startX, startY, endX, endY, algoritmo, color)

    def createsierpinsky(self, startX, startY, endX, endY, algoritmo, color):
        punto1 = Punto(startX, startY)
        punto2 = Punto((startX + endX) // 2, endY)
        punto3 = Punto(endX, startY)

        self.createsierpinskyrec(punto1, punto2, punto3, algoritmo, color)

    def createsierpinskyrec(self, p1, p2, p3, algoritmo, color, n=6):

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

    def createkotch(self, startX, startY, endX, endY, algoritmo, color):
        punto1 = Punto(startX, startY)
        punto2 = Punto(endX, startY)
        self.createkotchrec(punto1, punto2, algoritmo, color)

    def createkotchrec(self, p1, p4, algoritmo, color, n=5):

        if n == 0:
            self.addlinea(Linea(p1, p4, algoritmo, color), None)
        else:
            dx = (p4.getX() - p1.getX()) // 3
            dy = (p4.getY() - p1.getY()) // 3

            p2 = Punto(p1.getX() + dx, p1.getY() + dy)
            p3 = Punto(p2.getX() + dx, p2.getY() + dy)
            paux = Punto(((dx - math.sqrt(3) * dy) // 2) + (p1.getX() + dx), ((math.sqrt(3) * dx + dy) // 2) + (p1.getY() + dy))

            n -= 1

            self.createkotchrec(p1, p2, algoritmo, color, n)
            self.createkotchrec(p2, paux, algoritmo, color, n)
            self.createkotchrec(paux, p3, algoritmo, color, n)
            self.createkotchrec(p3, p4, algoritmo, color, n)

    def createmandelbrot(self, startX, startY, endX, endY, algoritmo, color):
        # ALGORITMO DE: https://www.codingame.com/playgrounds/2358/how-to-plot-the-mandelbrot-set/mandelbrot-set
        # Plot window
        RE_START = -2
        RE_END = 1
        IM_START = -1
        IM_END = 1

        for x in range(0, endX - startX):
            for y in prange(0, endY - startY):
                # Convert pixel coordinate to complex number
                c = complex(RE_START + (x / (endX - startX)) * (RE_END - RE_START),
                            IM_START + (y / (endY - startY)) * (IM_END - IM_START))
                # Compute the number of iterations
                m = self.mandelbrot(c)
                # The color depends on the number of iterations
                color = 255 - int(m * 255 / 256)
                # Plot the point
                self.addlinea(Linea(Punto(x + startX, y + startY), Punto(x + startX, y + startY), algoritmo,
                                    '#%02x%02x%02x' % (color, color, color)), None)

    def mandelbrot(self, c):
        z = 0
        n = 0
        while abs(z) <= 2 and n < 256:
            z = z * z + c
            n += 1
        return n

    def createjulia(self, startX, startY, endX, endY, algoritmo, color):
        #Algoritmo de: https://www.geeksforgeeks.org/julia-fractal-python/

        # setting up the variables according to
        # the equation to  create the fractal
        cX, cY = -0.7, 0.27015
        moveX, moveY = 0.0, 0.0

        w = endX - startX
        h = endY - startY
        zoom = 1

        for x in range(w):
            for y in range(h):
                zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + moveX
                zy = 1.0 * (y - h / 2) / (0.5 * zoom * h) + moveY
                i = 300
                while zx * zx + zy * zy < 4 and i > 1:
                    tmp = zx * zx - zy * zy + cX
                    zy, zx = 2.0 * zx * zy + cY, tmp
                    i -= 1
                # convert byte to RGB (3 bytes), kinda
                color = 255 - int(i * 255 / 300)
                # Plot the point
                self.addlinea(Linea(Punto(x + startX, y + startY), Punto(x + startX, y + startY), algoritmo,
                                    '#%02x%02x%02x' % (i, i, i)), None)