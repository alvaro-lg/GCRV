from GUI import GUI
from constantes import *
import tkinter as tk
import time

ventana= tk.Tk()
ventana.title("Práctica 1 - Álvaro López García")
app = GUI(master=ventana)
frecuencia = float(1 / FRAMERATE)

app.mainloop()