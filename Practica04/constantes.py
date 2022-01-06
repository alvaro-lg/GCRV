DEBUG = 0
DEFAULT_SCALE = 1
DEFAULT_ALGORITHM = 0
DEFAULT_MODE = 0
DEFAULT_COLOR = '#FF0000' # Red
DEFAULT_PRIMARY_COLOR = '#000000' # Black
DEFAULT_SECONDARY_COLOR = '#FF0000' # Red
CANVAS_BG = "white"
GUI_BG = '#eeeeee'
CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
MIN_RES = 1
MAX_RES = 64
MODOS = {"Edición" : 0, "Selección" : 1}
ALGORITMOS = {"Direct Scan Conversion" : 0, "Digital Differential Analyzer (DDA)" : 1, "Bresenham’s algorithm" : 2}
CABECERA_ANIMACIONES = ["Animacion", "Comienzo", "Final"]
FRAMERATE = 15
TIPOS_ANIMACION = {"Translation" : 0, "Scaling" : 1, "Rotation" : 2, "Shearing" : 3, "Reflexion" : 4}
TIPOS_FRACTAL = {"Triangulo de Sierpinsky" : 0, "Curva de Kotch" : 1, "Mandelbrot" : 2,  "Julia" : 3,
                 "Triangulo de Sierpinsky (IFS)" : 4, "Curva de Kotch (IFS)" : 5, "Barnsley's Fern (IFS)" : 6,
                 "Chaos (IFS)" : 7,
                 #"Alvaro (IFS)" : 8
                 }
ITERS_FRACTAL = {0: 6, 1: 5, 2: 256, 3: 256, 4: 30000, 5: 30000, 6: 500000, 7: 30000, 8: 1000}
INIT_SCALE_IFS = 1000