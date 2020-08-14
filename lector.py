#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : lector.py
# Author            : Carlos Carral <carloscarral13@gmail.com>
# Date              : 12/08/2020
# Last Modified Date: 12/08/2020
import csv
import json
from horarios import HorarioClase
import pprint
from materias import Materia
import random

IDS =["A","B","C","D","E","F","G","H","I","J","K","L", "M", "N", "O", "P", "Q", "R","S","T","U","V","W","X","Y","Z",
        "##","$$","%%","&&","//","==","??","**","~~","<<>>"] 

class LectorCSV:
    """
    Wrapper de la clase DictReader de csv.
    Toma como parámetros de entrada el nombre de un archivo csv.
    """

    def __init__(self):

        self.archivo = None
        self.dict_reader = None


    def __init__(self, csv_fname):
        self.set_archivo(csv_fname)

    def __del__(self):
        if self.archivo is not None:
            self.archivo.close()

    def set_archivo(self, nom_archivo) -> None:
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
        try:
            self.dict_reader = csv.DictReader(f=self.archivo, fieldnames=campos)
        except Error:
            raise CSVException("Error al hacer el parseo del archivo csv")


class LectorPlantilla(LectorCSV):
    def __init__(self, csv_fname):
        super().__init__(csv_fname)
        self.instanciar_dict_reader()
        self.available_ids = IDS.copy().reverse()

    def get_id(self):
        if  self.available_ids is None:
            return random.choice(IDS) 

        else:
            return self.available_ids.pop()

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

    def buscar_por_num(self, num: str)-> HorarioClase():
        """
        Regresa un HorarioClase()
        """

        fila = None
        dic_format = None

        self.archivo.seek(0)
        if self.dict_reader is None:
            raise DictReaderNoInstanciadoError

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

    def buscar_por_cve(self, cve) -> list():
        """
        Regresa una lista de HorarioClase() con cve=cve
        """
        if self.dict_reader is None:
            raise DictReaderNoInstanciadoError

        self.archivo.seek(0)
        lista_clases = list()

        for _fila in self.dict_reader:
            claves = [s.replace(" ","") for s in _fila["cve"].split("/")]
            #  claves =  _fila["cve"].split("/")
            print("Claves: {}, separadas: {}".format(_fila["cve"],claves))
            if cve in claves:
                lista_clases.append(_fila)

        if not lista_clases:
            print("Not found in plantilla: {}".format(cve))
            raise ValorNoEncontradoException(cve)

        return [self.instanciar_horario(fila) for fila in lista_clases]


    def instanciar_horario(self, fila) -> HorarioClase():
        h = HorarioClase(self.get_id())
        h.set_num(fila["num"])
        h.set_prof(fila["prof"])
        h.set_gpo(fila["gpo"])
        h.set_cve(fila["cve"])
        h.set_nombre_materia(fila["mat"])

        grid_dict = dict()

        inicio = None
        fin = None

        # TODO: Agregar Expresión regular que reconozca horas en formatos no normalizados
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
    def __init__(self, csv_fname):
        super().__init__(csv_fname)
        self.instanciar_dict_reader()

    def instanciar_dict_reader(self):
        campos = ["cve", "Materia"]
        super().instanciar_dict_reader(campos)

    def buscar_por_cve(self, cve):
        """
        Regresa un objeto Materia() con clave==cve
        Si no la encuentra, regresa una excepción.
        """

        m = None

        if self.dict_reader is None:
            raise DictReaderNoInstanciadoError

        self.archivo.seek(0)

        for fila in self.dict_reader:
            claves = [s.replace(" ", "") for s in fila["cve"].split('/')]
            if cve in claves:
                m = Materia(cve, fila["Materia"])
                break

        if m is None:
            print("Not found in materias: {}".format(cve))
            raise ValorNoEncontradoException(cve)

        return m


class LectorJSON:
    def __init__(self, json_fname):

        self.archivo = None
        self.set_archivo(json_fname)

        # Licenciatura
        self.lic = None

        # Lista de claves
        self.candidatos = list()

        # Num cursar
        self.num_cursar = int()

        # Semilla
        self.semilla = None

        self.parse_json()

    def get_candidatos(self):
        return self.candidatos

    def get_semilla(self):

        if self.semilla == "":
            return None
        else:
            return self.semilla

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
        self.msg = "Error en el archivo '{}'".format(nom_arch)


class DictReaderNoInstanciadoError(Exception):
    pass


class JSONException(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg


class CSVException(Exception):
    def __init__(self):
        super().__init__()
        self.msg = msg


class ValorNoEncontradoException(Exception):
    def __init__(self, val):
        super().__init__()
        self.msg = "No se pudo encontrar un elemento con clave {}".format(val)
