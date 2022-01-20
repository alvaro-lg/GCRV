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
                 "Chaos (IFS)" : 7, "Alvaro (IFS)" : 8, "Curva de Kotch (L-Sistema)" : 9,
                 "Triangulo de Sierpinsky (L-Sistema)" : 10, "Curva del Dragon (L-Sistema)" : 11,
                 "Alfombra de Sierpinsky (L-Sistema)" : 12, "Planta Fractal (L-Sistema)" : 13
                 }
ITERS_FRACTAL = {0: 6, 1: 5, 2: 256, 3: 256, 4: 30000, 5: 30000, 6: 500000, 7: 30000, 20: 1000, 8: 100000, 9: 5, 10: 10, 11: 10, 12: 5, 13: 5}
INIT_SCALE_IFS = 1000000