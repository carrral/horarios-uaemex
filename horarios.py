from datetime import datetime as dt
from prettytable import PrettyTable
import sys

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
    "07:00": 0,
    "07:30": 1,
    "08:00": 2,
    "08:30": 3,
    "09:00": 4,
    "09:30": 5,
    "10:00": 6,
    "10:30": 7,
    "11:00": 8,
    "11:30": 9,
    "12:00": 10,
    "12:30": 11,
    "13:00": 12,
    "13:30": 13,
    "14:00": 14,
    "14:30": 15,
    "15:00": 16,
    "15:30": 17,
    "16:00": 18,
    "16:30": 19,
    "17:00": 20,
    "17:30": 21,
    "18:00": 22,
    "18:30": 23,
    "19:00": 24,
    "19:30": 25,
    "20:00": 26,
    "20:30": 27,
    "21:00": 28,
    "21:30": 29,
}

DIAS_STR = ["lun", "mar", "mie", "jue", "vie", "sab"]

# ================================== #
#  Clase contenedora de un horario
# ================================== #


class Horario:
    def __init__(self):

        #  Arreglo 30x6 que guarda los espacios que
        #  ocupa un horario en una semana LUN-SAB 7:00-21:30

        self.grid = [[F for j in range(DIAS)] for i in range(BLOQUES_HORA)]

    def display(self):
        print_grid(self.grid)


class HorarioMaestro(Horario):
    def __init__(self, titulo):
        super().__init__()

        #  Identificador de un horario en particular.
        #  Más que nada el nombre para mostrar del horario en particular
        self.titulo = titulo
        self.merged = list()
        self.len = 0

    def get_titulo(self):
        return self.titulo

    def merge(self, horario):
        """
        Junta los grids del horario actual con @horario.
        Nota: Éste método no hace una revisión de la compatibilidad de los
        horarios, por lo tanto si no son compatibles, habrá sobreescritura
        """

        for i in range(BLOQUES_HORA):
            for j in range(DIAS):
                if self.grid[i][j] == F:
                    self.grid[i][j] = horario.grid[i][j]

        self.merged.append(horario)
        self.len += 1

    def display(self):
        super().display()
        pt = PrettyTable(field_names=["num", "cve","mat" ,"prof", "ID"])

        for h in self.merged:
            pt.add_row(h.get_attr_list())

        print(pt)


class HorarioClase(Horario):
    def __init__(self, x=X):
        """
        @x es el caracter que se utilizará para marcar
        los espacios que ocupará el horario ('X' por default)
        """
        super().__init__()

        self.num = None
        self.cve = None
        self.prof = None
        self.nombre_materia = None
        self.gpo = None
        self.x = x

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

    def set_nombre_materia(self, materia):
        self.materia = materia

    def get_nombre_materia(self):
        return self.materia

    def set_gpo(self, gpo):
        self.gpo = gpo

    def get_gpo(self):
        return self.gpo

    def set_grid(self, dict_horario: dict):
        """
        Crea el grid de la materia actual con un horario formateado de la
        siguiente manera:

        {"lun":(07:00,07:30),"mar":(09:00,11:00),...}

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
                self.grid[i][j] = self.x

    def get_grid(self) -> list:
        return self.grid

    def get_attr_list(self) -> list:
        l = list()
        l.append(self.num)
        l.append(self.cve)
        l.append(self.get_nombre_materia())
        l.append(self.prof)
        l.append(self.x)

        return l


class CaracterInvalidoException(Exception):
    pass


def print_grid(grid):
    dummy = DIAS_STR.copy()
    dummy.insert(0, " ")
    pt = PrettyTable(field_names=dummy, padding=8)
    bloques_list = list(BLOQUES_MAPEO.keys())
    for i in range(BLOQUES_HORA):
        l = grid[i].copy()
        l.insert(0, bloques_list[i])
        pt.add_row(l)

    print(pt)


def horarios_compatibles(a: Horario, b: Horario) -> bool:
    """
    Verifica que dos horarios sean compatibles entre sí
    (que no haya traslapes)
    Toma como argumentos dos objetos Horario()
    """
    for i in range(BLOQUES_HORA):
        for j in range(DIAS):
            if a.grid[i][j] != F and b.grid[i][j] != F:
                return False

    return True


def time_delta(a: str, b: str) -> int:
    """
    Regresa el número de minutos entre dos horas con el formato
    hhmm
    """
    fmt = "%H:%M"
    td_obj_1 = dt.strptime(a, fmt)
    td_obj_2 = dt.strptime(b, fmt)

    #  Regresa un objeto timedelta
    delta = (td_obj_1 - td_obj_2).seconds
    return int((delta / 60))


def init_grid(grid, libre: str = F):
    """
    Inicializa un grid con valores en blanco
    """

    for i in range(BLOQUES_HORA):
        for j in range(DIAS):
            grid[i][j] = libre


def error_out(msg: str):
    print("ERROR: {}\n".format(msg), file=sys.stderr)
