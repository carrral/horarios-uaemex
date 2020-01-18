import csv


class LectorWrapper:
    """
    Wrapper de la clase DictReader de csv.
    Toma como parámetros de entrada el nombre de un archivo csv.
    """

    def __init__(self):

        self.archivo = None
        self.dict_reader = None

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

    def instanciar_dict_reader(self):
        if self.archivo is None:
            raise Exception

        campos = [
            "num",
            "prof",
            "cve",
            "mat",
            "gpo",
            "cap",
            "ini_lun",
            "fin_lun",
            "ini_mar",
            "fin_mar",
            "ini_mie",
            "fin_mie",
            "ini_jue",
            "fin",
            "jue",
            "ini_vie",
            "fin_vie",
            "ini_sab",
            "fin_sab",
        ]

        self.dict_reader = csv.DictReader(f=self.archivo, fieldnames=campos)

    def buscar_por_num(self, num):
        """
        Regresa un diccionario formateado
        """

        fila = None
        dic_format = None

        if self.dict_reader is None:
            raise DictReadeNoInstanciadoError

        for _fila in self.dict_reader:
            if self.dict_reader["num"] == num:
                fila = _fila
                break

        dic_format = self.formatear_horario(fila)

        return dic_format

    def buscar_por_cve(self, cve):
        """
        Regresa una lista de diccionarios formateados
        """
        pass

    def formatear_horario(self, fila):
        pass


class ArchivoInexistenteError(Exception):
    def __init__(self, nom_arch):
        self.nom_arch = nom_arch


class DictReadeNoInstanciadoError(Exception):
    pass
