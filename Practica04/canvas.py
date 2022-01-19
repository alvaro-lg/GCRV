import time
import tkinter as tk
import numpy as np
from poligono import Poligono
from punto import Punto
from linea import Linea
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
        self.fractales = set()
        self.puntosTmp = list()
        self.poligonoTmp = Poligono()
        self.timeiter = float(0)
        self.period = float(1 / FRAMERATE) * 1000
        self.lineatarget = None
        self.poligonotarget = None
        self.playing = False
        self.img = tk.PhotoImage(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

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

            for y in range(startY, endY + sentido, sentido):
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

                for x in range(startX, endX + sentido, sentido):
                    ytrue = m * x + b
                    y = int(round(ytrue, 0))
                    puntos.append(Punto(x, y))
                    self.pintapixel(x, y, color=color)
            else:

                if startY < endY:
                    sentido = 1
                else:
                    sentido = -1

                for y in range(startY, endY + sentido, sentido):
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

            for y in range(startY, endY + sentido, sentido):
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

                for x in range(startX, endX + sentido, sentido):
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

                for y in range(startY, endY + sentido, sentido):
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

            for y in range(startY, endY + sentido, sentido):
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

            for i in range(0, longest, 1):
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

        for i in range(int(x + (CANVAS_WIDTH / 2)), int(x + self.scale + (CANVAS_WIDTH / 2)),\
                       np.sign(int(x + self.scale + (CANVAS_WIDTH / 2) - int(x + (CANVAS_WIDTH / 2))))):
            for j in range(int(-y + (CANVAS_HEIGHT / 2)), int(-(y + self.scale) + (CANVAS_HEIGHT / 2)),\
                           np.sign(int(-(y + self.scale) + (CANVAS_HEIGHT / 2) - int(-y + (CANVAS_HEIGHT / 2))))):
                if i > 0 and j > 0:
                    self.img.put(color, (i, j))

    def borrapixel(self, pixel):
        self.pintapixel(pixel.getX(), pixel.getY(), color=self['background'])

    def rescale(self, scale):
        self.scale = scale
        self.refresh()

    def refresh(self):
        self.img = tk.PhotoImage(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.pintafractales()
        self.pintapoligonos(set.union(self.poligonos, {self.poligonoTmp}))
        super().create_image((CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2), image=self.img, state="normal")

    def pintapoligonos(self, poligonos):
        for poligono in poligonos:
            lineas = poligono.getlineas()
            for linea in poligono.getlineas().keys():
                if lineas[linea] is None:
                    poligono.addlinea(linea, self.pintalinea(linea))
                else:
                    puntos = lineas[linea]
                    for punto in puntos:
                        self.pintapixel(punto.getX(), punto.getY(), color=linea.getcolor())

    def pintafractales(self):
        for fractal in self.fractales:
            pixeles = fractal.getpixels()
            if fractal.gettype() == 0 or fractal.gettype() == 1 or fractal.gettype() >= 4:
                for linea in pixeles:
                    self.pintalinea(linea)
            else:
                x, y = fractal.getabscoords()
                self.img.put(pixeles, (x, y))


    def scalepoint(self, x, y):
        return x - (x % self.scale),\
               y - (y % self.scale)

    def getpoligonos(self):
        return self.poligonos

    def setpoligonos(self, poligonosvalues):
        self.poligonos, self.puntosTmp, self.poligonoTmp, self.lineatarget, self.poligonotarget, self.fractales = poligonosvalues.getvalues()
        if DEBUG: print("Nuevos valores de los poligonos (" + str(len(self.poligonos)) + " poligonos en total): " + str(self.poligonos))
        self.refresh()
        if self.poligonotarget is not None: self.root.setanimationsvalues(self.poligonotarget.getanimaciones())
        
    def settargetcolor(self, color):
        if self.lineatarget is not None and self.root.getmode() == 1:
            self.lineatarget.setcolor(color)
            self.refresh()

    def setfractales(self, fractales):
        self.fractales = fractales

    def getsnapshot(self):
        return Snapshot(deepcopy(self.poligonos), deepcopy(self.puntosTmp), deepcopy(self.poligonoTmp),\
                        deepcopy(self.lineatarget), deepcopy(self.poligonotarget), deepcopy(self.fractales))

    def getpoligonotarget(self):
        return self.poligonotarget

    def play(self):
        self.playing = True
        endtime = 0

        if len(self.poligonos) > 0:
            poligonosanimated = deepcopy(self.poligonos)
            finales = [j.getend() for i in poligonosanimated for j in i.getanimaciones()]

            if len(finales) > 0:
                endtime = max(finales)

                while self.playing and self.timeiter <= (endtime * 1000):
                    t_start = time.time()
                    self.newframe(poligonosanimated)
                    self.timeiter += self.period
                    self.root.master.update()
                    t_end = time.time()
                    time.sleep(self.period / 1000 - (t_end - t_start) if self.period / 1000 - (t_end - t_start) > 0 else 0)

        if self.timeiter > (endtime * 1000) or endtime == 0:
            self.timeiter = float(0)
            self.root.playpause()

    def pause(self):
        self.playing = False

    def newframe(self, poligonosanimated):

        if DEBUG: print('Nuevo Frame: ' + str(self.timeiter / 1000) + 's')
        if DEBUG: print(poligonosanimated)

        self.img = tk.PhotoImage(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

        for poligono in poligonosanimated:
            for linea in poligono.getlineas().keys():
                newLinea = deepcopy(linea)
                for animation in poligono.getanimaciones():
                    newLinea = animation.applyanimation(newLinea, self.timeiter / 1000)
                self.pintalinea(newLinea)

        super().create_image((CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2), image=self.img, state="normal")
        self.root.master.update()

    def stop(self):
        self.timeiter = float(0)
        if self.playing: self.root.playpause()
        self.refresh()

    def isplaying(self):
        return self.playing

    def addanimacion(self, animation):
        if DEBUG: print('Animacion ' + str(animation.gettype()) + ' anhiadida a poligono: ' + str(self.poligonotarget))
        self.poligonotarget.addanimacion(animation)
        self.root.takesnapshot()

    def removeanimacion(self, animation):
        if DEBUG: print('Animacion ' + str(animation.gettype()) + ' eliminada de poligono: ' + str(self.poligonotarget))
        self.poligonotarget.removeanimacion(animation)

    def preview(self, animacion):
        self.poligonotarget.addanimacion(deepcopy(animacion))
        self.timeiter = float((animacion.getstart() * 1000))
        self.play()
        self.poligonotarget.removeanimacion(animacion)

    def addfractal(self, fractal):
        self.fractales.add(fractal)
        self.refresh()
        self.root.takesnapshot()