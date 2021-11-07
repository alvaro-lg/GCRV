from copy import deepcopy
from canvas import Canvas
from constantes import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import tkinter as tk
from snapshot import snapshot


class GUI(tk.Frame):
    def __init__(self, bg_color=GUI_BG, master=None):
        super().__init__(master)
        super().configure(bg=bg_color)
        self.master = master
        self.bg = bg_color
        self.pack()
        self.create_widgets()
        self.snaps = list()
        self.snapsNum = 0
        self.bind_all("<Control-z>", self.undo)
        self.bind_all("<Control-y>", self.redo)

    def create_widgets(self):

        # Creación del slider de la escala
        self.textscale = tk.Label(self, text='Tamaño del píxel:', bg=self.bg)
        self.scalechooser = tk.Scale(self, from_=MIN_RES, to=MAX_RES, bg=self.bg,
                                     orient='horizontal', command=self.rescalecanvas)

        # Mode selection
        self.textmode = tk.Label(self, text='Modo:', bg=self.bg)
        self.modeselector = ttk.Combobox(self, state="readonly", values=list(MODOS.keys()), width=10)
        self.modeselector.current(0)

        # Algorithm selection
        self.textalgorithm = tk.Label(self, text='Algoritmo:', bg=self.bg)
        self.algorithmselector = ttk.Combobox(self, state="readonly", values=list(ALGORITMOS.keys()), width=10)
        self.algorithmselector.current(0)

        # Color pickers
        self.color1 = tk.Canvas(self, width=60, height=60, bg=DEFAULT_PRIMARY_COLOR)
        self.color1.bind("<Button 1>", self.pickcolor)
        self.color2 = tk.Canvas(self, width=40, height=40, bg=DEFAULT_SECONDARY_COLOR)
        self.color2.bind("<Button 1>", self.switchcolors)

        # Creación del canvas
        self.canvas = Canvas(self)

        # Layout
        self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvas.grid(column=0, row=0, columnspan=3, rowspan=8, sticky=(tk.N, tk.S, tk.W))
        self.textscale.grid(column=3, row=0, pady=(50, 10), sticky=(tk.S, tk.E, tk.W))
        self.scalechooser.grid(column=4, row=0, pady=(50, 10), sticky=(tk.N, tk.E, tk.W))
        self.textmode.grid(column=3, row=2, pady=(0, 10), sticky=(tk.W))
        self.modeselector.grid(column=4, row=2, pady=(0, 10), sticky=(tk.E))
        self.textalgorithm.grid(column=3, row=3, pady=(0, 300), sticky=(tk.N, tk.W))
        self.algorithmselector.grid(column=4, row=3, pady=(0, 300), sticky=(tk.N, tk.E))
        self.color1.grid(column=3, row=5, pady=(0, 50), sticky=(tk.E))
        self.color2.grid(column=4, row=5, pady=(0, 50), sticky=(tk.W))

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(1, weight=1)

    def rescalecanvas(self, value):
        self.canvas.rescale(int(value))

    def pickcolor(self, event):
        self.color1['background'] = askcolor(title="Choose color")[-1]
        self.canvas.settargetcolor(self.color1['background'])

    def switchcolors(self, event):
        tmp = self.color1['background']
        self.color1['background'] = self.color2['background']
        self.color2['background'] = tmp
        self.canvas.settargetcolor(self.color1['background'])

    def getcolor(self):
        return self.color1['background']

    def getmode(self):
        return MODOS[self.modeselector.get()]

    def getalgorithm(self):
        return ALGORITMOS[self.algorithmselector.get()]

    def getscale(self):
        return self.scalechooser.get()

    def undo(self, event):
        if DEBUG: print('Undo')

        if len(self.snaps) > 0 and self.snapsNum - 1 > 0:
            snap = self.snaps[self.snapsNum - 1]
            self.canvas.setlineas(snap.getvalues())
            self.canvas.update_idletasks()
            self.snapsNum -= 1

    def redo(self, event):
        if DEBUG: print('Redo')

        if len(self.snaps) > 0 and self.snapsNum < len(self.snaps):
            snap = self.snaps[self.snapsNum + 1]
            self.canvas.setlineas(snap.getvalues())
            self.canvas.update_idletasks()
            self.snapsNum += 1

    def takesnapshot(self):
        if DEBUG: print('Snapshot')
        self.snaps.append(snapshot(deepcopy(self.canvas.getlineas())))
        self.snapsNum += 1