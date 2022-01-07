import time
from copy import deepcopy

from animation import Animation
from canvas import Canvas
from constantes import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk

from fractal import Fractal


class GUI(tk.Frame):
    def __init__(self, bg_color=GUI_BG, master=None):
        super().__init__(master)
        super().configure(bg=bg_color)
        self.master = master
        self.bg = bg_color
        self.pack()
        self.create_widgets()
        self.snapsUndo = list()
        self.snapsRedo = list()
        self.bind_all("<Control-z>", self.undo)
        self.bind_all("<Control-y>", self.redo)
        self.takesnapshot()

    def create_widgets(self):

        # Creación del slider de la escala
        self.textscale = tk.Label(self, text='Tamaño del píxel:', bg=self.bg)
        self.scalechooser = tk.Scale(self, from_=MIN_RES, to=MAX_RES, bg=self.bg,
                                     orient='horizontal', command=self.rescalecanvas)

        # Mode selection
        self.textmode = tk.Label(self, text='Modo:', bg=self.bg)
        self.modeselector = ttk.Combobox(self, state="readonly", values=list(MODOS.keys()), width=10)
        self.modeselector.current(DEFAULT_MODE)

        # Algorithm selection
        self.textalgorithm = tk.Label(self, text='Algoritmo:', bg=self.bg)
        self.algorithmselector = ttk.Combobox(self, state="readonly", values=list(ALGORITMOS.keys()), width=10)
        self.algorithmselector.current(DEFAULT_ALGORITHM)

        # Color pickers
        self.color1 = tk.Canvas(self, width=50, height=50, bg=DEFAULT_PRIMARY_COLOR)
        self.color1.bind("<Button 1>", self.pickcolor)
        self.color2 = tk.Canvas(self, width=35, height=35, bg=DEFAULT_SECONDARY_COLOR)
        self.color2.bind("<Button 1>", self.switchcolors)

        # Panel donde se muestran las animaciones del poligono targeteado
        self.animationspanel = ttk.Treeview(columns=CABECERA_ANIMACIONES, show="headings")
        for col in CABECERA_ANIMACIONES:
            self.animationspanel.heading(col, text=col)
            self.animationspanel.column(col, minwidth=0, width=70, stretch=False)
        vsb = ttk.Scrollbar(orient="vertical",  command=self.animationspanel.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.animationspanel.xview)
        self.animationspanel.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Play-Pause
        original_play_img = Image.open("./resources/play.png")
        original_play_img = original_play_img.resize((30, 30), Image.ANTIALIAS)
        play_img = ImageTk.PhotoImage(original_play_img)
        original_pause_img = Image.open("./resources/pause.png")
        original_pause_img = original_pause_img.resize((30, 30), Image.ANTIALIAS)
        pause_img = ImageTk.PhotoImage(original_pause_img)
        self.playbtn = tk.Button(self, width=40, height=40, image=play_img, command=self.playpause)
        self.imageplay = play_img
        self.imagepause = pause_img

        # Stop
        original_stop_img = Image.open("./resources/stop.png")
        original_stop_img = original_stop_img.resize((30, 30), Image.ANTIALIAS)
        stop_img = ImageTk.PhotoImage(original_stop_img)
        self.stopbtn = tk.Button(self, width=40, height=40, image=stop_img, command=self.stop)
        self.stopbtn.image = stop_img

        # Añadir animaciones
        self.btnanimation = tk.Button(self, text="Añadir animación", bg=self.bg,
                                      highlightbackground=self.bg, padx=10, pady=10, command=self.animationform)

        # Añadir animaciones
        self.btnfractal = tk.Button(self, text="Añadir fractal", bg=self.bg,
                                      highlightbackground=self.bg, padx=10, pady=10, command=self.fractalform)

        # Creación del canvas
        self.canvas = Canvas(self)

        # Layout
        self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvas.grid(column=0, row=0, columnspan=3, rowspan=10, sticky=(tk.N, tk.S, tk.W))
        self.textscale.grid(column=3, row=0, pady=(50, 10), sticky=(tk.S, tk.E, tk.W))
        self.scalechooser.grid(column=4, row=0, pady=(50, 10), sticky=(tk.N, tk.E, tk.W))
        self.textmode.grid(column=3, row=2, pady=(0, 5), sticky=(tk.W))
        self.modeselector.grid(column=4, row=2, pady=(0, 5), sticky=(tk.E))
        self.textalgorithm.grid(column=3, row=3, pady=(0, 50), sticky=(tk.N, tk.W))
        self.algorithmselector.grid(column=4, row=3, pady=(0, 50), sticky=(tk.N, tk.E, tk.S))
        self.color1.grid(column=3, row=4, pady=(0, 100), sticky=(tk.E))
        self.color2.grid(column=4, row=4, pady=(0, 100), sticky=(tk.W))
        self.animationspanel.grid(column=3, row=5, columnspan=2, in_=self, sticky=("n"))
        self.playbtn.grid(column=3, row=6, pady=(0, 100), sticky=(tk.E))
        self.stopbtn.grid(column=4, row=6, pady=(0, 100), sticky=(tk.W))
        self.btnanimation.grid(column=3, row=7, pady=(0, 5), columnspan=2)
        self.btnfractal.grid(column=3, row=8, pady=(0, 30), columnspan=2)

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

        if len(self.snapsUndo) > 0:
            snapTmp = self.snapsUndo.pop(-1)
            self.snapsRedo.append(snapTmp)
            self.canvas.setpoligonos(snapTmp)

    def redo(self, event):
        if DEBUG: print('Redo')

        if len(self.snapsRedo) > 0:
            snapTmp = self.snapsRedo.pop(-1)
            self.snapsUndo.append(snapTmp)
            self.canvas.setpoligonos(snapTmp)

    def takesnapshot(self):
        if DEBUG: print('Snapshot:')
        if DEBUG: print(str([i for i in deepcopy(self.canvas.getpoligonos())]))
        self.snapsUndo.append(self.canvas.getsnapshot())
        self.snapsRedo.clear()

    def playpause(self):
        if self.canvas.isplaying():
            self.playbtn.configure(image=self.imageplay)
            self.canvas.pause()
        else:
            self.playbtn.configure(image=self.imagepause)
            self.canvas.play()

    def stop(self):
        self.canvas.stop()

    def setanimationsvalues(self, animations):
        self.animationspanel.delete(*self.animationspanel.get_children())
        for a in animations:
            self.animationspanel.insert("", tk.END, values=(list(TIPOS_ANIMACION.keys())[a.gettype()], a.getstart(), a.getend()))

    def animationform(self):

        self.poligonoanimated = self.canvas.getpoligonotarget()

        if self.poligonoanimated is not None and self.getmode() == 1:
            self.form = tk.Toplevel(master=self.master)

            self.form.configure(bg=self.bg)
            self.form.tipoanimacion = tk.Label(self.form, text='Tipo', bg=self.bg)
            self.form.startanimacion = tk.Label(self.form, text='Inicio \n Animacion (s)', bg=self.bg)
            self.form.endanimacion = tk.Label(self.form, text='Final \n Animacion (s)', bg=self.bg)
            self.form.vecxtext = tk.Label(self.form, text='Vector \n Transformacion (x)', bg=self.bg)
            self.form.vecytext = tk.Label(self.form, text='Vector \n Transformacion (y)', bg=self.bg)
            self.form.textanimacion = tk.Label(self.form, text='Animacion:', bg=self.bg)
            self.form.tiposelector = ttk.Combobox(self.form, state="readonly", values=list(TIPOS_ANIMACION.keys()), width=10)
            self.form.starttime = tk.Entry(self.form, width=10, highlightbackground=self.bg)
            self.form.endtime = tk.Entry(self.form, width=10, highlightbackground=self.bg)
            self.form.vecx = tk.Entry(self.form, width=10, highlightbackground=self.bg)
            self.form.vecy = tk.Entry(self.form, width=10, highlightbackground=self.bg)
            self.form.tiposelector.current(0)
            self.form.btnprevisualizar = tk.Button(self.form, text="Previsualizar animación", bg=self.bg,
                                                   highlightbackground=self.bg, padx=5, pady=5, command=self.previsualize)
            self.form.btnanhiadir = tk.Button(self.form, text="Añadir animación", bg=self.bg,
                                          highlightbackground=self.bg, padx=5, pady=5, command=self.addanimation)

            self.form.tipoanimacion.grid(column=1, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.startanimacion.grid(column=2, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.endanimacion.grid(column=3, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.vecxtext.grid(column=4, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.vecytext.grid(column=5, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.textanimacion.grid(column=0, row=1, padx=(30, 0), pady=(0, 20), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.tiposelector.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.starttime.grid(column=2, row=1, sticky=(tk.N, tk.E, tk.W))
            self.form.endtime.grid(column=3, row=1, sticky=(tk.N, tk.E, tk.W))
            self.form.vecx.grid(column=4, row=1, sticky=(tk.N, tk.E, tk.W))
            self.form.vecy.grid(column=5, row=1, sticky=(tk.N, tk.E, tk.W))
            self.form.btnprevisualizar.grid(column=6, row=0, pady=(20, 0), padx=(0, 30), sticky=(tk.N, tk.S))
            self.form.btnanhiadir.grid(column=6, row=1, padx=(0, 30), sticky=(tk.N, tk.E, tk.W))

    def addanimation(self):
        if float(self.form.endtime.get()) > float(self.form.starttime.get()) >= 0:
            animation = Animation(self.form.tiposelector.current(), float(self.form.starttime.get()),
                                  float(self.form.endtime.get()), int(self.form.vecx.get()), int(self.form.vecy.get()))
            self.canvas.addanimacion(animation)
            self.setanimationsvalues(self.canvas.getpoligonotarget().getanimaciones())
            self.form.destroy()
            self.canvas.refresh()

    def previsualize(self):
        if float(self.form.endtime.get()) > float(self.form.starttime.get()) >= 0:
            animation = Animation(self.form.tiposelector.current(), float(self.form.starttime.get()),
                                  float(self.form.endtime.get()), int(self.form.vecx.get()), int(self.form.vecy.get()))
            self.canvas.preview(animation)

    def fractalform(self):
        if self.getmode() == 0:
            self.form = tk.Toplevel(master=self.master)

            self.form.configure(bg=self.bg)
            self.form.tipofractallbl = tk.Label(self.form, text='Tipo', bg=self.bg)
            self.form.startXlbl = tk.Label(self.form, text='Coordenadas \n Iniciales (x0)', bg=self.bg)
            self.form.startYlbl = tk.Label(self.form, text='Coordenadas \n Iniciales (y0)', bg=self.bg)
            self.form.endXlbl = tk.Label(self.form, text='Coordenadas \n Finales (x1)', bg=self.bg)
            self.form.endYlbl = tk.Label(self.form, text='Coordenadas \n Finales (y1)', bg=self.bg)
            self.form.textfractal = tk.Label(self.form, text='Fractal:', bg=self.bg)
            self.form.tiposelector = ttk.Combobox(self.form, state="readonly", values=list(TIPOS_FRACTAL.keys()), width=25)
            self.form.startX = tk.Entry(self.form, width=10, highlightbackground=self.bg)
            self.form.startY = tk.Entry(self.form, width=10, highlightbackground=self.bg)
            self.form.endX = tk.Entry(self.form, width=10, highlightbackground=self.bg)
            self.form.endY = tk.Entry(self.form, width=10, highlightbackground=self.bg)
            self.form.tiposelector.current(0)

            self.form.btncrear = tk.Button(self.form, text="Crear fractal", bg=self.bg,
                                          highlightbackground=self.bg, padx=5, pady=5, command=self.addfractal)

            self.form.tipofractallbl.grid(column=1, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.startXlbl.grid(column=2, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.startYlbl.grid(column=3, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.endXlbl.grid(column=4, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.endYlbl.grid(column=5, row=0, pady=(20, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.textfractal.grid(column=0, row=1, padx=(30, 0), pady=(0, 20), sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.tiposelector.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
            self.form.startX.grid(column=2, row=1, sticky=(tk.N, tk.E, tk.W))
            self.form.startY.grid(column=3, row=1, sticky=(tk.N, tk.E, tk.W))
            self.form.endX.grid(column=4, row=1, sticky=(tk.N, tk.E, tk.W))
            self.form.endY.grid(column=5, row=1, sticky=(tk.N, tk.E, tk.W))
            self.form.btncrear.grid(column=6, row=1, padx=(0, 30), sticky=(tk.N, tk.E, tk.W))

    def addfractal(self):
        fractal = Fractal(self.form.tiposelector.current(), int(self.form.startX.get()),
                              int(self.form.startY.get()), int(self.form.endX.get()), int(self.form.endY.get()), self.getalgorithm(), self.getcolor())
        self.canvas.addfractal(fractal)
        self.form.destroy()