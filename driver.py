from prettytable import PrettyTable
import lector as ls

LIM_SUPERIOR_CURSAR = 8
PLANTILLA_ICO = "recursos/plantilla_ico_2020A.csv"
MATERIAS_ICO = "recursos/materias_ico_2020A.csv"


class Driver:
    def __init__(self):
        self.lector_json = None
        self.nombre_arch_plantilla = None
        self.nombre_arch_materias = None
        self.lector_materias = None
        self.lector_plantilla = None

        # Lista de objetos Materia()
        self.materias = list()

        # Lista de listas de HorarioClase()
        self.candidatos = list()
        self.semilla = None

        self.lic = None
        self.num_cursar = 0

    def main(self, json_fname):
        self.parse_json(json_fname)
        self.parse_conf(json_fname)
        self.display_conf()

    def parse_json(self, json_fname):
        self.lector_json = ls.LectorJSON(json_fname)

    def parse_conf(self, json_fname):
        """
        Inicializa la configuración del archivo json.
        Aquí se agrupan todas las excepciones que podrían surgir
        """
        # Obtener nombre de los archivos csv
        self.parse_lic()

        self.init_materias()

        self.init_plantilla()

        self.parse_candidatos()

        self.parse_semilla()

        self.parse_num_cursar()

    def init_materias(self):
        self.lector_materias = ls.LectorMaterias(self.nombre_arch_materias)

    def init_plantilla(self):
        """
        Inicializa el lector de la plantilla
        """
        self.lector_plantilla = ls.LectorPlantilla(self.nombre_arch_plantilla)

    def display_materias(self):
        print(
            """
        *==========================================*
                    Materias Elegidas
        *==========================================*"""
        )
        pt = PrettyTable(["cve", "Nombre"])
        for materia in self.materias:
            pt.add_row(materia.get_attr_list())

        print(pt)

    def display_semilla(self):
        print(
            """
        *==========================================*
                       Licenciatura
        *==========================================*

                           {}""".format(
                self.lic.upper()
            )
        )

        print(
            """
        *==========================================*
                        Prioridad 
        *==========================================*"""
        )
        if self.semilla is None:
            print(
                """
             *----------------------------------*
               No se eligió horario a priorizar
             *----------------------------------*"""
            )
        else:
            pt = PrettyTable(["num", "prof", "cve", "gpo"])
            fila = [
                self.semilla.num,
                self.semilla.prof,
                self.semilla.cve,
                self.semilla.gpo,
            ]
            pt.add_row(fila)
            print(pt)

    def display_conf(self):
        self.display_semilla()
        self.display_materias()

        print(
            """
        *==========================================*
            Num. de Materias a cursar: {}
        *==========================================*""".format(
                self.num_cursar
            )
        )

    def get_num_cursar(self):
        return self.num_cursar

    def parse_candidatos(self):
        """
        Inicializa self.candidatos con una lista de listas de HorarioClase()
        """
        # TODO manejo de excepciones (llamado sin inicializar)
        cves_candidatos = self.lector_json.get_candidatos()
        for cve in cves_candidatos:
            self.candidatos.append(self.lector_plantilla.buscar_por_cve(cve))
            self.materias.append(self.lector_materias.buscar_por_cve(cve))

    def get_candidatos(self) -> list:
        return self.candidatos

    def parse_semilla(self):
        # TODO manejo de excepciones (llamado sin inicializar)

        num = self.lector_json.get_semilla()

        if num is not None:
            self.semilla = self.lector_plantilla.buscar_por_num(num)

        else:
            self.semilla = None

    def get_semilla(self):
        return self.semilla

    def parse_lic(self):
        self.lic = self.lector_json.lic

        if self.lic.lower() == "ico":
            self.nombre_arch_plantilla = PLANTILLA_ICO
            self.nombre_arch_materias = MATERIAS_ICO

        else:
            raise NoSoportadoException("licenciatura", self.lic)

    def parse_num_cursar(self):
        # TODO Manejo de excepciones
        # TODO getter para num_cursar
        self.num_cursar = self.lector_json.num_cursar

        if self.num_cursar <= 0:
            raise CondicionesException(
                "El número de materias a cursar no puede ser menor a 1"
            )

        if self.num_cursar > len(self.materias):
            raise CondicionesException(
                """
            El numero de materias  a cursar ({}) no puede ser mayor
            que el número de candidatos ({})""".format(
                    self.num_cursar, len(self.materias)
                )
            )


class CondicionesException(Exception):
    def __init__(self, cond):
        super().__init__()
        self.msg = "La siguiente condición no pudo ser agregada:\n    {}".format(cond)


class NoSoportadoException(Exception):
    def __init__(self, opc, val):
        super().__init__()
        self.msg = "Opción no soportada todavía: {} = {}".format(opc, val)
