import time
import tkinter as tk
from datetime import datetime

from numba.cuda import target

from poligono import Poligono
from punto import Punto
from linea import Linea
from numba import prange
from constantes import *
from copy import deepcopy
from snapshot import Snapshot

class Canvas(tk.Canvas):

    def __init__(self, root):
        super().__init__(root, bg=CANVAS_BG, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.bind("<Button 1>", self.onclick)
        self.bind("<Button 2>", self.newform)
        self.root = root
        self.scale = root.getscale()
        self.poligonos = set()
        self.puntosTmp = list()
        self.poligonoTmp = Poligono()
        self.lineatarget = None
        self.poligonotarget = None
        self.playing = False

    def onclick(self, event):

        self.root.takesnapshot()

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
            self.poligonoTmp.addlinea(lineatmp, self.pintalinea(lineatmp))
            self.lineatarget = lineatmp
            self.puntosTmp.pop(0)

    def newform(self, event):
        self.poligonos.add(deepcopy(self.poligonoTmp))
        self.poligonoTmp = Poligono()
        self.puntosTmp.clear()

    def onclickseleccion(self, punto):
        
        self.newform(None)
        x, y, = self.scalepoint(punto.getX(), punto.getY())

        # Recorremos las lineas buscando la del punto
        for poligono in set.union(self.poligonos, {self.poligonoTmp}):
            if DEBUG: print('...seleccionando linea targeteada...')
            for linea in poligono.getlineas().keys():
                if DEBUG: print(linea)
                puntos = poligono.getlineas()[linea]
                for i in puntos:
                    j, k = self.scalepoint(i.getX(), i.getY())
                    if x == j and y == k:
                        self.lineatarget = linea
                        self.pintalinea(self.lineatarget)
                        self.poligonotarget = poligono
                        self.root.setanimationsvalues(self.poligonotarget.getanimaciones())
                        if DEBUG: print('Pintando linea targeteada: ' + str(self.lineatarget))
                        return

        # Caso de que no se escoja ninnguna linea
        self.lineatarget = None
        self.poligonotarget = None
        self.root.setanimationsvalues([])

    def pintalinea(self, linea):

        # Switch-Case con el algoritmo con el que queremos pintar la recta
        switch = {
            0 : self.pintalinea1,
            1 : self.pintalinea2,
            2 : self.pintalinea3
        }

        func = switch[linea.getalgoritmo()]

        if self.lineatarget is not None and linea.equals(self.lineatarget) and self.root.getmode() == 1:
            color = linea.getcomplementaryColor()
        else:
            color = linea.getcolor()

        puntos = func(linea, color)

        if DEBUG: print(str(len(puntos)) + ' Puntos: ' + str(puntos))

        return puntos

    def pintalinea1(self, linea, color):

        if DEBUG: print('Algoritmo 1')

        # Escogemos los puntos arbitrariamente
        startX, startY = linea.getstart().getX(), linea.getstart().getY()
        endX, endY = linea.getend().getX(), linea.getend().getY()

        puntos = list()

        # Caso de la linea vertical
        if startX == endX:

            if startY < endY:
                sentido = 1
            else:
                sentido = -1

            x = int(round(startX, 0))

            for y in prange(startY, endY + sentido, sentido):
                puntos.append(Punto(x, y))
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
                    puntos.append(Punto(x, y))
                    self.pintapixel(x, y, color=color)
            else:

                if startY < endY:
                    sentido = 1
                else:
                    sentido = -1

                for y in prange(startY, endY + sentido, sentido):
                    xtrue = (y - b) / m
                    x = int(round(xtrue, 0))
                    puntos.append(Punto(x, y))
                    self.pintapixel(x, y, color=color)
        return puntos

    def pintalinea2(self, linea, color):

        if DEBUG: print('Algoritmo 2')

        # Escogemos los puntos arbitrariamente
        startX, startY = linea.getstart().getX(), linea.getstart().getY()
        endX, endY = linea.getend().getX(), linea.getend().getY()

        puntos = list()

        # Caso de la linea vertical
        if startX == endX:

            if startY < endY:
                sentido = 1
            else:
                sentido = -1

            x = int(round(startX, 0))

            for y in prange(startY, endY + sentido, sentido):
                puntos.append(Punto(x, y))
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
                    puntos.append(Punto(x, y))
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
                    puntos.append(Punto(x, y))
                    self.pintapixel(x, y, color=color)

        return puntos


    def pintalinea3(self, linea, color):

        if DEBUG: print('Algoritmo 3')

        # Escogemos los puntos arbitrariamente
        startX, startY = linea.getstart().getX(), linea.getstart().getY()
        endX, endY = linea.getend().getX(), linea.getend().getY()

        puntos = list()

        # Caso de la linea vertical
        if startX == endX:

            if startY < endY:
                sentido = 1
            else:
                sentido = -1

            x = int(round(startX, 0))

            for y in prange(startY, endY + sentido, sentido):
                puntos.append(Punto(x, y))
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
                puntos.append(Punto(startX, startY))
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
        self.pintapoligonos(set.union(self.poligonos, {self.poligonoTmp}))

    def pintapoligonos(self, poligonos):
        for poligono in poligonos:
            for linea in poligono.getlineas().keys():
                poligono.addlinea(linea, self.pintalinea(linea))


    def scalepoint(self, x, y):
        return x - (x % self.scale),\
               y - (y % self.scale)

    def getpoligonos(self):
        return self.poligonos

    def setpoligonos(self, poligonosvalues):
        self.poligonos, self.puntosTmp, self.poligonoTmp, self.lineatarget, self.poligonotarget = poligonosvalues.getvalues()
        print("Nuevos valores de los poligonos (" + str(len(self.poligonos)) + " poligonos en total): " + str(self.poligonos))
        self.refresh()
        
    def settargetcolor(self, color):
        if self.lineatarget is not None and self.root.getmode() == 1:
            self.lineatarget.setcolor(color)
            self.refresh()

    def getsnapshot(self):
        return Snapshot(deepcopy(self.poligonos), deepcopy(self.puntosTmp), deepcopy(self.poligonoTmp),\
                        deepcopy(self.lineatarget), deepcopy(self.poligonotarget))

    def getpoligonotarget(self):
        return self.poligonotarget

    def play(self):
        self.playing = True
        self.timeiter = float(0)
        self.poligonosanimated = deepcopy(self.poligonos)

        period = float(1 / FRAMERATE) * 1000
        endtime = max(j.getend() for i in self.poligonosanimated for j in i.getanimaciones())

        while self.playing and self.timeiter <= (endtime * 1000):
            t_start = time.time()
            self.newframe()
            self.timeiter += period
            self.root.master.update()
            t_end = time.time()
            time.sleep(period / 1000 - (t_end - t_start) if period / 1000 - (t_end - t_start) > 0 else 0)

    def pause(self):
        self.playing = False

    def newframe(self):

        super().delete('all')

        if DEBUG: print('Nuevo Frame: ' + str(self.timeiter / 1000) + 's')
        if DEBUG: print(self.poligonosanimated)

        for poligono in self.poligonosanimated:
            for animation in poligono.getanimaciones():
                for linea in poligono.getlineas().keys():
                    self.pintalinea(animation.applyanimation(linea, self.timeiter / 1000))

    def stop(self):
        self.timeiter = float(0)
        self.refresh()
        self.playing = False

    def isplaying(self):
        return self.playing

    def addanimacion(self, animation):
        if DEBUG: print('Animacion ' + str(animation.gettype()) + ' anhiadida a poligono: ' + str(self.poligonotarget))
        self.poligonotarget.addanimacion(animation)