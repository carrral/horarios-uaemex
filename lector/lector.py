import csv
import json
from horarios.horarios import HorarioClase
import pprint


class LectorCSV:
    """
    Wrapper de la clase DictReader de csv.
    Toma como parámetros de entrada el nombre de un archivo csv.
    """

    def __init__(self):

        self.archivo = None
        self.dict_reader = None

    def __del__(self):
        if self.archivo is not None:
            self.archivo.close()

    def set_archivo(self, nom_archivo):
        """
        Abre el archivo csv para lectura
        """

        # Cualquier excepción que  se genere
        # será manejada por el método driver superior
        try:
            self.archivo = open(nom_archivo, "r")
        except FileNotFoundError:
            raise ArchivoInexistenteError(nom_archivo)

    def instanciar_dict_reader(self, campos):
        if self.archivo is None:
            raise Exception
        self.dict_reader = csv.DictReader(f=self.archivo, fieldnames=campos)

    def buscar_por_cve(self, cve):
        """
        Regresa una lista de diccionarios formateados
        """
        pass


class LectorPlantilla(LectorCSV):
    def instanciar_dict_reader(self):
        campos = [
            "num",
            "prof",
            "cve",
            "mat",
            "gpo",
            "ini_lun",
            "fin_lun",
            "ini_mar",
            "fin_mar",
            "ini_mie",
            "fin_mie",
            "ini_jue",
            "fin_jue",
            "ini_vie",
            "fin_vie",
            "ini_sab",
            "fin_sab",
        ]

        super().instanciar_dict_reader(campos)

    def buscar_por_num(self, num: str):
        """
        Regresa un HorarioClase()
        """

        fila = None
        dic_format = None

        if self.dict_reader is None:
            raise DictReadeNoInstanciadoError

        for _fila in self.dict_reader:
            #  print(_fila)
            if _fila["num"] == num:
                fila = _fila
                break

        if fila is None:
            # TODO: Excepción?
            pass

        horario = self.instanciar_horario(fila)

        return horario

    def instanciar_horario(self, fila):
        h = HorarioClase()
        h.set_num(fila["num"])
        h.set_prof(fila["prof"])
        h.set_gpo(fila["gpo"])
        h.set_cve(fila["cve"])

        grid_dict = dict()

        i = -1
        inicio = None
        fin = None

        values_list = [(key, val) for key, val in fila.items()]
        values_list = values_list[5:]
        values_list = [(key[4:], val) for key, val in values_list if val != ""]

        for index in range(0, len(values_list), 2):
            dia, hr_ini = values_list[index]
            dia, hr_fin = values_list[index + 1]
            grid_dict[dia] = (hr_ini, hr_fin)

        h.set_grid(grid_dict)

        return h


class LectorMaterias(LectorCSV):
    pass


class LectorJSON:
    def __init__(self):
        self.archivo = None
        self.data = None
        self.lic = None

        # Lista de claves
        self.candidatos = list()

        # Num cursar
        self.num_cursar = int()

        # Semilla
        self.semilla = None

    def __del__(self):
        self.archivo.close()

    def set_archivo(self, nom_archivo):

        try:
            self.archivo = open(nom_archivo, "r")
            self.data = json.load(self.archivo)

        except:
            raise ArchivoInexistenteError(nom_archivo)

    def parse_json(self):

        try:
            json_data = self.data

            self.candidatos = list(json_data["candidatos"])
            self.lic = json_data["licenciatura"]
            self.num_cursar = json_data["num_cursar"]
            self.semilla = json_data["prioridad"]

        except JSONDecodeError:
            raise JSONException("Error en archivo JSON")


class ArchivoInexistenteError(Exception):
    def __init__(self, nom_arch):
        super().__init__()
        self.nom_arch = nom_arch


class DictReadeNoInstanciadoError(Exception):
    pass


class JSONException(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg
