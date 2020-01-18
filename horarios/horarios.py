from datetime import datetime as dt

# ============= #
#  Constantes
# ============= #

#  Número de bloques de hora en  los que se divide el día
#  7:00,7:30,8:00,8:30,...,9:30
BLOQUES_HORA = 30

# Número de días de lunes a sábado
DIAS = 6

# Caracter que marca bloque ocupado
X = "X"
# Caracter que marca bloque disponible
F = " "

# Mapeo de los bloques de horario con su índice
BLOQUES_MAPEO = {
    "0700": 0,
    "0730": 1,
    "0800": 2,
    "0830": 3,
    "0900": 4,
    "0930": 5,
    "1000": 6,
    "1030": 7,
    "1100": 8,
    "1130": 9,
    "1200": 10,
    "1230": 11,
    "1300": 12,
    "1330": 13,
    "1400": 14,
    "1430": 15,
    "1500": 16,
    "1530": 17,
    "1600": 18,
    "1630": 19,
    "1700": 20,
    "1730": 21,
    "1800": 22,
    "1830": 23,
    "1900": 24,
    "1930": 25,
    "2000": 26,
    "2030": 27,
    "2100": 28,
    "2130": 29,
}

DIAS_STR = ["lun", "mar", "mie", "jue", "vie", "sab"]

# ================================== #
#  Clase contenedora de un horario
# ================================== #


class Horario:
    def __init__(self):
        self.prof = None
        self.cve = None
        self.num = None
        self.materia = None
        self.gpo = None

        #  Arreglo 30x6 que guarda los espacios que
        #  ocupa un horario en una semana LUN-SAB 7:00-21:30

        self.grid = [[F for j in range(DIAS)] for i in range(BLOQUES_HORA)]

    #  Setters y getters

    def set_prof(self, nom_prof):
        self.prof = nom_prof

    def get_prof(self):
        return self.prof

    def set_cve(self, cve):
        self.cve = cve

    def get_cve(self):
        return self.cve

    def set_num(self, num):
        self.num = num

    def get_num(self):
        return self.num

    def set_materia(self, materia):
        self.materia = materia

    def get_materia(self):
        return self.materia

    def set_gpo(self, gpo):
        self.gpo = gpo

    def get_gpo(self):
        return self.gpo

    def set_grid(self, dict_horario):
        """
        Crea el grid de la materia actual con un horario formateado de la
        siguiente manera:

        {"lun":(0700,0730),"mar":(0900,1100),...}

        """
        init_grid(self.grid)

        for dia in dict_horario.keys():
            # Obtener el número de bloques por día

            # Tuple (ini, fin)
            horario_dia = dict_horario[dia]
            inicio = horario_dia[0]
            fin = horario_dia[1]

            num_bloques = int(time_delta(fin, inicio) / 30)

            j = DIAS_STR.index(dia)

            index_inicio = BLOQUES_MAPEO[inicio]
            index_fin_range = index_inicio + num_bloques

            for i in range(index_inicio, index_fin_range):
                self.grid[i][j] = 'X'


def print_grid(grid):
    for fila in grid:
        print("\n")
        print(fila)

def horarios_compatibles(a, b):
    """
    Verifica que dos horarios sean compatibles entre sí
    (que no haya traslapes)
    Toma como argumentos dos objetos Horario()
    """
    for i in range(BLOQUES_HORA):
        for j in range(DIAS):
            if a.grid[i][j] == X and b.grid[i][j] == X:
                return False

    return True


def time_delta(a, b):
    """
    Regresa el número de minutos entre dos horas con el formato
    hhmm
    """
    fmt = "%H%M"
    td_obj_1 = dt.strptime(a, fmt)
    td_obj_2 = dt.strptime(b, fmt)

    #  Regresa un objeto timedelta
    delta = (td_obj_1 - td_obj_2).seconds
    return int((delta / 60))


def init_grid(grid):
    """
    Inicializa un grid con valores en blanco
    """

    for i in range(BLOQUES_HORA):
        for j in range(DIAS):
            grid[i][j] = F
