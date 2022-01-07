import math
from copy import deepcopy
import numpy as np
from random import randint
from constantes import DEBUG, ITERS_FRACTAL, CANVAS_WIDTH, CANVAS_HEIGHT, INIT_SCALE_IFS
from linea import Linea
from punto import Punto
import tkinter as tk

class Fractal:
    def __init__(self, type, startX, startY, endX, endY, algoritmo, color):
        # Dimensiones absolutas de nuestra imagen
        self.width = abs(endX - startX)
        self.height = abs(endY - startY)
        self.x = startX
        self.y = endY

        self.pixels = ""
        self.type = type
        self.generatepixels(startX, startY, endX, endY, algoritmo, color)

    def gettype(self):
        return self.type

    def getpixels(self):
        return self.pixels

    def getabscoords(self):
        return int(self.x + (CANVAS_WIDTH / 2)), int(-self.y + (CANVAS_HEIGHT / 2))

    def generatepixels(self, startX, startY, endX, endY, algoritmo, color):

        switch = {
            0: self.createsierpinsky,
            1: self.createkotch,
            2: self.createmandelbrot,
            3: self.createjulia,
            4: self.createsierpinskyIFS,
            5: self.createkotchIFS,
            6: self.createbansleyIFS,
            7: self.createchaosIFS,
            20: self.createalvaroIFS,
            8: self.createkotchLSys,
            9: self.createsierpinskyLSys,
            10: self.createdragonLSys,
            11: self.createsierpinskycarpetLSys,
            12: self.createfractplantLSys
        }

        if DEBUG: print('Creando fractal: ' + str(self.type))

        switch[self.type](startX, startY, endX, endY, algoritmo, color)

    def createsierpinsky(self, startX, startY, endX, endY, algoritmo, color):
        punto1 = Punto(startX, startY)
        punto2 = Punto((startX + endX) // 2, endY)
        punto3 = Punto(endX, startY)

        self.pixels = list()

        self.createsierpinskyrec(punto1, punto2, punto3, algoritmo, color, ITERS_FRACTAL[self.type])

    def createsierpinskyrec(self, p1, p2, p3, algoritmo, color, n):

        if n == 0:
            self.pixels.append(Linea(p1, p2, algoritmo, color))
            self.pixels.append(Linea(p2, p3, algoritmo, color))
            self.pixels.append(Linea(p3, p1, algoritmo, color))
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

        self.pixels = list()

        self.createkotchrec(punto1, punto2, algoritmo, color, ITERS_FRACTAL[self.type])

    def createkotchrec(self, p1, p4, algoritmo, color, n):

        if n == 0:
            self.pixels.append(Linea(p1, p4, algoritmo, color))
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

        # Parametros de la region de mandelbrot que queremos generar
        xa = -2.0; xb = 1.0
        ya = -1.5; yb = 1.5

        xmandel = [xa + (xb - xa) * kx / self.width for kx in range(self.width)]
        ymandel = [ya + (yb - ya) * ky / self.height for ky in range(self.height)]

        self.pixels = " ".join(("{" + " ".join(('#%02x%02x%02x' % self.mandel(i, j, color) for i in xmandel)) + "}" for j in ymandel))

    def mandel(self, kx, ky, color):
        """ calculates the pixel color of the point of mandelbrot plane
            passed in the arguments """

        color = color[1:]
        color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

        maxIt = 256
        c = complex(kx, ky)
        z = complex(0.0, 0.0)

        i = ITERS_FRACTAL[self.type]

        while i > 1 and abs(z) < 2.0:
            z = z * z + c
            i -= 1

        # convert byte to RGB (3 bytes), kinda
        i0 = i + int(((255 - i) * color[0]) / ITERS_FRACTAL[self.type])
        i1 = i + int(((255 - i) * color[1]) / ITERS_FRACTAL[self.type])
        i2 = i + int(((255 - i) * color[2]) / ITERS_FRACTAL[self.type])

        return (i0, i1, i2)

    def createjulia(self, startX, startY, endX, endY, algoritmo, color):
        #Algoritmo de: https://www.geeksforgeeks.org/julia-fractal-python/
        color = color[1:]
        color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

        # setting up the variables according to
        # the equation to  create the fractal
        cX, cY = -0.7, 0.27015
        #cX, cY = random.uniform(-1, 1), random.uniform(-1, 1)
        if DEBUG: print('Coeficientes para Julia: ' + cX + ', ' + cY)

        moveX, moveY = 0.0, 0.0

        w = self.width
        h = self.height
        zoom = 1

        self.pixels = " "

        for y in range(h):
            self.pixels += " { "
            for x in range(w):
                zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + moveX
                zy = 1.0 * (y - h / 2) / (0.5 * zoom * h) + moveY
                i = ITERS_FRACTAL[self.type]
                while zx * zx + zy * zy < 4 and i > 1:
                    tmp = zx * zx - zy * zy + cX
                    zy, zx = 2.0 * zx * zy + cY, tmp
                    i -= 1
                # convert byte to RGB (3 bytes), kinda
                i0 = i + int(((255 - i) * color[0]) / ITERS_FRACTAL[self.type])
                i1 = i + int(((255 - i) * color[1]) / ITERS_FRACTAL[self.type])
                i2 = i + int(((255 - i) * color[2]) / ITERS_FRACTAL[self.type])

                # Plot the point
                self.pixels += ('#%02x%02x%02x' % (i0, i1, i2))
                self.pixels += ' '
            self.pixels += " }"

    def createsierpinskyIFS(self, startX, startY, endX, endY, algoritmo, color):

        funciones = [[np.array([[0.5, 0.],
                                [0., 0.5]]), np.array([-1., 1.])],
                  [np.array([[0.5, 0.],
                            [0., 0.5]]), np.array([1., 1.])],
                  [np.array([[0.5, 0.],
                            [0., 0.5]]), np.array([0., -1.])]]

        self.pixels = list()
        n = ITERS_FRACTAL[self.type]
        coords = np.array([0, 0])

        for i in range(n):
            transformation = randint(1, len(funciones)) - 1
            newcoords = funciones[transformation][0] @ coords.T + funciones[transformation][1].T
            self.pixels.append(Linea(Punto(-INIT_SCALE_IFS * newcoords[0], -INIT_SCALE_IFS * newcoords[1]), Punto(-INIT_SCALE_IFS * newcoords[0], -INIT_SCALE_IFS * newcoords[1]), algoritmo, color))
            coords = newcoords

        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def createkotchIFS(self, startX, startY, endX, endY, algoritmo, color):

        funciones = [[np.array([[0.333, 0.0], [0.0, 0.333]]), np.array([0.0, 0.0])],
                [np.array([[0.167, -0.288], [0.288, 0.167]]), np.array([0.333, 0.0])],
                [np.array([[0.167, 0.288], [-0.288, 0.167]]), np.array([0.5, 0.288])],
                [np.array( [[.333, 0.], [0., .333]]), np.array([.667, 0.])]]

        self.pixels = list()
        n = ITERS_FRACTAL[self.type]
        coords = np.array([0, 0])

        for i in range(n):
            transformation = randint(1, len(funciones)) - 1
            newcoords = funciones[transformation][0] @ coords.T + funciones[transformation][1].T
            self.pixels.append(Linea(Punto(INIT_SCALE_IFS * newcoords[0], INIT_SCALE_IFS * newcoords[1]),
                                     Punto(INIT_SCALE_IFS * newcoords[0], INIT_SCALE_IFS * newcoords[1]),
                                     algoritmo, color))
            coords = newcoords

        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def createbansleyIFS(self, startX, startY, endX, endY, algoritmo, color):

        funciones = [[np.array([[0.81, 0.07], [-0.04, 0.84]]), np.array([0.12, 0.195])],
                [np.array([[0.18, -0.25], [0.27, 0.23]]), np.array([0.12, 0.02])],
                [np.array([[0.19, 0.275], [0.238, -0.14]]), np.array([0.16, 0.12])],
                [np.array( [[0.0235, 0.087], [0.045, 1/6]]), np.array([0.11, 0.0])]]

        self.pixels = list()
        n = ITERS_FRACTAL[self.type]
        coords = np.array([0, 0])

        for i in range(n):
            transformation = randint(1, len(funciones)) - 1
            newcoords = funciones[transformation][0] @ coords.T + funciones[transformation][1].T
            self.pixels.append(Linea(Punto(INIT_SCALE_IFS * newcoords[0], INIT_SCALE_IFS * newcoords[1]),
                                     Punto(INIT_SCALE_IFS * newcoords[0], INIT_SCALE_IFS * newcoords[1]),
                                     algoritmo, color))
            coords = newcoords

        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def createchaosIFS(self, startX, startY, endX, endY, algoritmo, color):

        funciones = [[np.array([[0, 0.053], [-0.429, 0]]), np.array([-7.083, 5.43])],
                    [np.array([[0.143, 0], [0, -0.053]]), np.array([-5.619, 8.513])],
                    [np.array([[0.143, 0], [0, 0.083]]), np.array([-5.619, 2.057])],
                    [np.array([[0, 0.053], [0.429, 0]]), np.array([-3.952, 5.43])],
                    [np.array([[0.119, 0], [0, 0.053]]), np.array([-2.555, 4.536])],
                    [np.array([[-0.0123806, -0.0649723], [0.423819, 0.00189797]]), np.array([-1.226, 5.235])],
                    [np.array([[0.0852291, 0.0506328], [0.420449, 0.0156626]]), np.array([-0.421, 4.569])],
                    [np.array([[0.104432, 0.00529117], [0.0570516, 0.0527352]]), np.array([0.976, 8.113])],
                    [np.array([[-0.00814186, -0.0417935], [0.423922, 0.00415972]]), np.array([1.934, 5.37])],
                    [np.array([[0.093, 0], [0, 0.053]]), np.array([0.861, 4.536])],
                    [np.array([[0, 0.053], [-0.429, 0]]), np.array([2.447, 5.43])],
                    [np.array([[0.119, 0], [0, -0.053]]), np.array([3.363, 8.513])],
                    [np.array([[0.119, 0], [0, 0.053]]), np.array([3.363, 1.487])],
                    [np.array([[0, 0.053], [0.429, 0]]), np.array([3.972, 4.569])],
                    [np.array([[0.123998, -0.00183957], [0.000691208, 0.0629731]]), np.array([6.275, 7.716])],
                    [np.array([[0, 0.053], [0.167, 0]]), np.array([5.215, 6.483])],
                    [np.array([[0.071, 0], [0, 0.053]]), np.array([6.279, 5.298])],
                    [np.array([[0, -0.053], [-0.238, 0]]), np.array([6.805, 3.714])],
                    [np.array([[-0.121, 0], [0, 0.053]]), np.array([5.941, 1.487])]]

        self.pixels = list()
        n = ITERS_FRACTAL[self.type]
        coords = np.array([0, 0])

        for i in range(n):
            transformation = randint(1, len(funciones)) - 1
            newcoords = funciones[transformation][0] @ coords.T + funciones[transformation][1].T
            self.pixels.append(Linea(Punto(INIT_SCALE_IFS * newcoords[0], INIT_SCALE_IFS * newcoords[1]),
                                     Punto(INIT_SCALE_IFS * newcoords[0], INIT_SCALE_IFS * newcoords[1]),
                                     algoritmo, color))
            coords = newcoords

        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def createalvaroIFS(self, startX, startY, endX, endY, algoritmo, color):

        funciones = [np.array([[0.07175926, 0., 0.], [0.13888889, 0.16666667, 0.], [0., 0., 1.]]),
                    np.array([[0.07175926, 0., 0.07175926], [-0.13888889, 0.16666667, 0.13888889], [0., 0., 1.]]),
                    np.array([[0.05740741, 0., 0.04305556], [0., 0.16666667, 0.05555556], [0., 0., 1.]]),
                    np.array([[8.78797472e-18, 1.43518519e-01, 1.71296296e-01], [-1.66666667e-01, 1.02053900e-17, 1.66666667e-01], [0., 0., 1.]]),
                    np.array([[0.11959877, 0., 0.19521605], [0., 0.16666667, 0. ], [0., 0., 1.]]),
                    np.array([[0.07175926, 0., 0.34259259], [-0.13888889, 0.16666667, 0.13888889], [0., 0., 1.]]),
                    np.array([[0.07175926, 0., 0.41435185], [0.13888889, 0.16666667, 0.], [0., 0., 1.]]),
                    np.array([[0.07175926, 0., 0.51388889], [0.13888889, 0.16666667, 0.], [0., 0.9, 1.]]),
                    np.array([[0.07175926, 0., 0.58564815], [-0.13888889, 0.16666667, 0.13888889], [0., 0., 1.]]),
                    np.array([[8.78797472e-18, 1.43518519e-01, 6.85185185e-01], [-1.66666667e-01, 1.02053900e-17, 1.66666667e-01], [0., 0., 1.]]),
                    np.array([[0.09567901, 0., 0.70910494], [0., 0.125, 0.14583333], [0., 0., 1.]]),
                    np.array([[4.39398736e-18, 1.43518519e-01, 8.04783951e-01], [-8.33333333e-02, 1.02053900e-17, 1.66666667e-01], [0., 0., 1.]]),
                    np.array([[0.09567901, 0., 0.70910494], [0., 0.125, 0.08333333], [0., 0., 1.]]),
                    np.array([[0.11959877, 0., 0.70910494], [-0.05555556, 0.16666667, 0.05555556], [0., 0., 1.]]),
                    np.array([[0.09567901, 0., 0.88040123], [0., 0.16666667, 0.], [0., 0., 1.]]),
                    np.array([[8.78797472e-18, -1.43518519e-01, 1.00000000e+00], [1.66666667e-01, 1.02053900e-17, 0.00000000e+00], [0., 0., 1.]]),
                    np.array([[0.09567901, 0., 0.88040123], [0., 0.16666667, 0.13888889], [0., 0., 1.]]),
                    np.array([[8.78797472e-18, -1.43518519e-01, 8.80401235e-01], [1.66666667e-01, 1.02053900e-17, 0.00000000e+00], [0., 0., 1.]])]

        self.pixels = list()
        n = ITERS_FRACTAL[self.type]
        coords = np.array([0, 0, 1])
        head_start = 100

        for i in range(head_start):  # do `head_start` iterations to start converging
            coords = (funciones[randint(1, len(funciones)) - 1]) @ coords

        for i in range(n):
            newcoords = (funciones[randint(1, len(funciones)) - 1]) @ coords
            print(newcoords)
            self.pixels.append(Linea(Punto(INIT_SCALE_IFS * newcoords[0], INIT_SCALE_IFS * newcoords[1]),
                                     Punto(INIT_SCALE_IFS * newcoords[0], INIT_SCALE_IFS * newcoords[1]),
                                     algoritmo, color))
            coords = newcoords

        print(self.pixels[1000:2000])
        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def createkotchLSys(self, startX, startY, endX, endY, algoritmo, color):

        self.pixels = list()

        system_rules = {"F": "F+F-F-F+F"}
        terminal_symbols = {"+": np.array([[0, -1], [1, 0]]), "-": np.array([[0, 1], [-1, 0]])}

        word = "F"

        for _ in range(ITERS_FRACTAL[self.type]):
            word_aux = str()
            for i in range(0, len(word)):
                if word[i] not in terminal_symbols.keys() and system_rules[word[i]]:
                    word_aux += system_rules[word[i]]
                else:
                    word_aux += word[i]
            word = word_aux

        dir = np.array([1, 0])
        coords = np.array([1, 1])

        for i in range(0, len(word)):
            if word[i] in terminal_symbols.keys():
                dir = terminal_symbols[word[i]] @ dir.T
            else:
                start = coords
                end = start + dir * INIT_SCALE_IFS
                self.pixels.append(Linea(Punto(start[0], start[1]), Punto(end[0], end[1]), algoritmo, color))
                coords = end

        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def createsierpinskyLSys(self, startX, startY, endX, endY, algoritmo, color):

        self.pixels = list()

        system_rules = {"A": "B-A-B", "B": "A+B+A"}
        terminal_symbols = {"+": np.array([[math.cos(math.radians(60)), -math.sin(math.radians(60))],
                                           [math.sin(math.radians(60)), math.cos(math.radians(60))]]),
                            "-": np.array([[math.cos(math.radians(300)), -math.sin(math.radians(300))],
                                           [math.sin(math.radians(300)), math.cos(math.radians(300))]])}

        word = "A"

        for _ in range(ITERS_FRACTAL[self.type]):
            word_aux = str()
            for i in range(0, len(word)):
                if word[i] not in terminal_symbols.keys() and system_rules[word[i]]:
                    word_aux += system_rules[word[i]]
                else:
                    word_aux += word[i]
            word = word_aux

        dir = np.array([1, 0])
        coords = np.array([1, 1])

        for i in range(0, len(word)):
            if word[i] in terminal_symbols.keys():
                dir = terminal_symbols[word[i]] @ dir.T
            else:
                start = coords
                end = start + dir * INIT_SCALE_IFS
                self.pixels.append(Linea(Punto(start[0], start[1]), Punto(end[0], end[1]), algoritmo, color))
                coords = end

        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def createdragonLSys(self, startX, startY, endX, endY, algoritmo, color):

        self.pixels = list()

        system_rules = {"X": "X+YF+", "Y": "-FX-Y"}
        terminal_symbols = {"+": np.array([[0, -1], [1, 0]]), "-": np.array([[0, 1], [-1, 0]])}

        word = "FX"

        for _ in range(ITERS_FRACTAL[self.type]):
            word_aux = str()
            for i in range(0, len(word)):
                if word[i] not in terminal_symbols.keys() and word[i] in system_rules.keys():
                    word_aux += system_rules[word[i]]
                else:
                    word_aux += word[i]
            word = word_aux

        dir = np.array([1, 0])
        coords = np.array([1, 1])

        for i in range(0, len(word)):
            if word[i] in terminal_symbols.keys():
                dir = terminal_symbols[word[i]] @ dir.T
            elif word[i] == "F":
                start = coords
                end = start + dir * INIT_SCALE_IFS
                self.pixels.append(Linea(Punto(start[0], start[1]), Punto(end[0], end[1]), algoritmo, color))
                coords = end

        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def createsierpinskycarpetLSys(self, startX, startY, endX, endY, algoritmo, color):

        self.pixels = list()

        system_rules = {"f": "f+f-f-f-g+f+f+f-f", "g": "ggg"}
        terminal_symbols = {"+": np.array([[0, -1], [1, 0]]), "-": np.array([[0, 1], [-1, 0]])}

        word = "f"

        for _ in range(ITERS_FRACTAL[self.type]):
            word_aux = str()
            for i in range(0, len(word)):
                if word[i] not in terminal_symbols.keys() and word[i] in system_rules.keys():
                    word_aux += system_rules[word[i]]
                else:
                    word_aux += word[i]
            word = word_aux

        dir = np.array([1, 0])
        coords = np.array([1, 1])

        for i in range(0, len(word)):
            if word[i] in terminal_symbols.keys():
                dir = terminal_symbols[word[i]] @ dir.T
            else:
                start = coords
                end = start + dir * INIT_SCALE_IFS
                self.pixels.append(Linea(Punto(start[0], start[1]), Punto(end[0], end[1]), algoritmo, color))
                coords = end

        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def createfractplantLSys(self, startX, startY, endX, endY, algoritmo, color):

        self.pixels = list()

        system_rules = {"F": "FF", 'X': 'F-[[X]+X]+F[+FX]-X'}
        terminal_symbols = {"+": np.array([[math.cos(math.radians(25)), -math.sin(math.radians(25))],
                                           [math.sin(math.radians(25)), math.cos(math.radians(25))]]),
                            "-": np.array([[math.cos(math.radians(335)), -math.sin(math.radians(335))],
                                           [math.sin(math.radians(335)), math.cos(math.radians(335))]])}

        word = "X"

        for _ in range(ITERS_FRACTAL[self.type]):
            word_aux = str()
            for i in range(0, len(word)):
                if word[i] not in terminal_symbols.keys() and word[i] in system_rules.keys():
                    word_aux += system_rules[word[i]]
                else:
                    word_aux += word[i]
            word = word_aux

        dir = np.array([0., 1.])
        coords = np.array([1., 1.])
        lapiz = [coords, dir]
        stack = []

        for i in range(0, len(word)):

            if word[i] in terminal_symbols.keys():
                lapiz[1] = terminal_symbols[word[i]] @ lapiz[1].T
            if word[i] == "[":
                stack.append(deepcopy(lapiz))
            if word[i] == "]":
                lapiz = stack.pop()
            else:
                start = lapiz[0]
                end = start + lapiz[1] * INIT_SCALE_IFS
                self.pixels.append(Linea(Punto(start[0], start[1]), Punto(end[0], end[1]), algoritmo, color))
                lapiz[0] = end

        self.standarizeIFSpoints(startX, startY, endX, endY, algoritmo, color)

    def standarizeIFSpoints(self, startX, startY, endX, endY, algoritmo, color):

        maxX = max(max(i.getstart().getX(), i.getend().getX()) for i in self.pixels)
        maxY = max(max(i.getstart().getY(), i.getend().getY()) for i in self.pixels)
        minX = min(min(i.getstart().getX(), i.getend().getX()) for i in self.pixels)
        minY = min(min(i.getstart().getY(), i.getend().getY()) for i in self.pixels)
        pixelsaux = deepcopy(self.pixels)
        self.pixels = list()

        scaleX = (abs(startX) + abs(endX)) / (abs(minX) + abs(maxX))
        scaleY = (abs(startY) + abs(endY)) / (abs(minY) + abs(maxY))

        for linea in pixelsaux:

            oldstartX, oldstartY = linea.getstart().getX(), linea.getstart().getY()
            oldendX, oldendY = linea.getend().getX(), linea.getend().getY()
            newstartX = (oldstartX + abs(minX)) * scaleX - abs(startX)
            newendX = (oldendX + abs(minX)) * scaleX - abs(startX)
            newstartY = (oldstartY + abs(minY)) * scaleY - abs(startY)
            newendY = (oldendY + abs(minY)) * scaleY - abs(startY)

            self.pixels.append(Linea(Punto(newstartX, newstartY), Punto(newendX, newendY), algoritmo, color))
