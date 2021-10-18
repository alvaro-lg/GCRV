import tkinter as tk
from punto import Punto
from linea import Linea
from numba import prange
from constantes import *
from copy import deepcopy

class Canvas(tk.Canvas):

    def __init__(self, root):
        super().__init__(root, bg=CANVAS_BG, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.bind("<Button 1>", self.onclick)
        self.root = root
        self.scale = root.getscale()
        self.lineas = dict()
        self.puntosTmp = list()
        self.lineatarget = None

    def onclick(self, event):

        self.root.takesnapshot()

        for i in range(self.root.snapsNum + 1, len(self.root.snaps)):
            self.root.snaps[i] = None

        punto = Punto(int(event.x - (CANVAS_WIDTH / 2)), int(-(event.y - (CANVAS_HEIGHT / 2))))

        switch = {
            0 : self.onclickedicion,
            1 : self.onclickseleccion
        }

        func = switch[self.root.getmode()]
        func(punto)

        self.refresh()

    def onclickedicion(self, punto):

        self.puntosTmp.append(punto)

        if DEBUG: print(self.puntosTmp[-1].getX(), self.puntosTmp[-1].getY())

        if len(self.puntosTmp) >= 2:
            lineatmp = Linea(self.puntosTmp[0], self.puntosTmp[1], self.root.getalgorithm(), self.root.getcolor())
            self.pintalinea(lineatmp)
            self.lineatarget = lineatmp
            self.puntosTmp[0] = self.puntosTmp[1]
            self.puntosTmp.pop(1)
            self.puntosTmp.clear()

    def onclickseleccion(self, punto):

        x, y, = self.scalepoint(punto.getX(), punto.getY())

        # Recorremos las lineas buscando la del punto
        for linea in self.lineas.keys():
            puntos = self.lineas[linea]
            for punto in puntos:
                xtemp, ytemp = self.scalepoint(punto.getX(), punto.getY())
                if x == xtemp and y == ytemp:
                    self.lineatarget = deepcopy(linea)
                    self.pintalinea(self.lineatarget)
                    return

        # Caso de que no se escoja ninnguna linea
        self.lineatarget = None

    def pintalinea(self, linea):

        # Switch-Case con el algoritmo con el que queremos pintar la recta
        switch = {
            0 : self.pintalinea1,
            1 : self.pintalinea2,
            2 : self.pintalinea3
        }

        func = switch[linea.getalgoritmo()]

        puntos = func(linea)
        self.lineas[linea] = puntos

    def pintalinea1(self, linea):

        if DEBUG: print('Algoritmo 1')

        if linea == self.lineatarget and self.root.getmode() == 1:
            color = linea.getcomplementaryColor()
        else:
            color = linea.getcolor()

        # Escogemos los puntos arbitrariamente
        startX, startY = linea.getstart().getX(), linea.getstart().getY()
        endX, endY = linea.getend().getX(), linea.getend().getY()

        puntos = set()

        # Caso de la linea vertical
        if startX == endX:

            if startY < endY:
                sentido = 1
            else:
                sentido = -1

            x = int(round(startX, 0))

            for y in prange(startY, endY + sentido, sentido):
                puntos.add(Punto(x, y))
                self.pintapixel(x, y, color=color)
        else:

            # Calculamos la pendiente y la ordenada en el origen
            m = (endY - startY) / (endX - startX)
            b = startY - (m * startX)

            if abs(m) < 1: # Pintamos la linea dependiendo del octante y el sentido

                if startX < endX:
                    sentido = 1
                else:
                    sentido = -1

                for x in prange(startX, endX + sentido, sentido):
                    ytrue = m * x + b
                    y = int(round(ytrue, 0))
                    puntos.add(Punto(x, y))
                    self.pintapixel(x, y, color=color)
            else:

                if startY < endY:
                    sentido = 1
                else:
                    sentido = -1

                for y in prange(startY, endY + sentido, sentido):
                    xtrue = (y - b) / m
                    x = int(round(xtrue, 0))
                    puntos.add(Punto(x, y))
                    self.pintapixel(x, y, color=color)
        return puntos

    def pintalinea2(self, linea):

        if DEBUG: print('Algoritmo 2')

        if linea == self.lineatarget and self.root.getmode() == 1:
            color = linea.getcomplementaryColor()
        else:
            color = linea.getcolor()

        # Escogemos los puntos arbitrariamente
        startX, startY = linea.getstart().getX(), linea.getstart().getY()
        endX, endY = linea.getend().getX(), linea.getend().getY()

        puntos = set()

        # Caso de la linea vertical
        if startX == endX:

            if startY < endY:
                sentido = 1
            else:
                sentido = -1

            x = int(round(startX, 0))

            for y in prange(startY, endY + sentido, sentido):
                puntos.add(Punto(x, y))
                self.pintapixel(x, y, color=color)
        else:

            # Calculamos la pendiente y la ordenada en el origen
            m = (endY - startY) / (endX - startX)
            b = startY - (m * startX)

            if abs(m) <= 1:

                if startX < endX:
                    sentido = 1
                else:
                    sentido = -1

                ytrue = startY

                for x in prange(startX, endX + sentido, sentido):
                    ytrue = ytrue + (m * sentido)
                    y = int(round(ytrue, 0))
                    puntos.add(Punto(x, y))
                    self.pintapixel(x, y, color=color)
            else:

                if startY < endY:
                    sentido = 1
                else:
                    sentido = -1

                xtrue = startX

                for y in prange(startY, endY + sentido, sentido):
                    xtrue = xtrue + ((1 / m) * sentido)
                    x = int(round(xtrue, 0))
                    puntos.add(Punto(x, y))
                    self.pintapixel(x, y, color=color)

        return puntos


    def pintalinea3(self, linea):

        if DEBUG: print('Algoritmo 3')

        if linea == self.lineatarget and self.root.getmode() == 1:
            color = linea.getcomplementaryColor()
        else:
            color = linea.getcolor()

        # Escogemos los puntos arbitrariamente
        startX, startY = linea.getstart().getX(), linea.getstart().getY()
        endX, endY = linea.getend().getX(), linea.getend().getY()

        puntos = set()

        # Caso de la linea vertical
        if startX == endX:

            if startY < endY:
                sentido = 1
            else:
                sentido = -1

            x = int(round(startX, 0))

            for y in prange(startY, endY + sentido, sentido):
                puntos.add(Punto(x, y))
                self.pintapixel(x, y, color=color)

        else:

            w = endX - startX
            h = endY - startY
            dx1 = dy1 = dx2 = dy2 = 0

            if w < 0: dx1 = -1
            elif w > 0: dx1 = 1

            if h < 0: dy1 = -1
            elif h > 0: dy1 = 1

            if w < 0: dx2 = -1
            elif w > 0: dx2 = 1

            longest = abs(w)
            shortest = abs(h)

            if not (longest > shortest):
                longest = abs(h)
                shortest = abs(w)
                if h < 0: dy2 = -1
                elif h > 0: dy2 = 1
                dx2 = 0

            numerator = longest >> 1

            for i in prange(0, longest, 1):
                puntos.add(Punto(startX, startY))
                self.pintapixel(startX, startY, color=color)
                numerator += shortest
                if not (numerator < longest):
                    numerator -= longest
                    startX += dx1
                    startY += dy1
                else:
                    startX += dx2
                    startY += dy2

        return puntos

    def borralinea(self, linea):

        for p in self.lineas[linea]:
            self.borrapixel(p)

    def pintapixel(self, x, y, color=DEFAULT_COLOR):

        x, y = self.scalepoint(x, y)
        
        super().create_rectangle(int(x + (CANVAS_WIDTH / 2)), int(-y + (CANVAS_HEIGHT / 2)),
            int(x + self.scale + (CANVAS_WIDTH / 2)), int(-(y + self.scale) + (CANVAS_HEIGHT / 2)),
                outline="", fill=color)
        
    def borrapixel(self, pixel):
        self.pintapixel(pixel.getX(), pixel.getY(), color=self['background'])

    def rescale(self, scale):
        self.scale = scale
        self.refresh()

    def refresh(self):
        super().delete("all")
        for linea in self.lineas.keys():
            self.pintalinea(linea)

    def scalepoint(self, x, y):
        return x - (x % self.scale),\
               y - (y % self.scale)

    def getlineas(self):
        return self.lineas

    def setlineas(self, lineasvalues):
        self.lineas = lineasvalues
        self.refresh()
        self.lineatarget = None
        
    def settargetcolor(self, color):
        if self.lineatarget is not None and self.root.getmode() == 1:
            self.lineatarget.setcolor(color)
            self.refresh()
            self.pintalinea(self.lineatarget)