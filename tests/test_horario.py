import unittest
from pprint import pprint
from horarios import horarios as hs
from lector import lector as lc

TEST_FILE = "recursos/plantilla_ico_2020A.csv"
TEST_JSON = "configuracion.json"


class HorariosTest(unittest.TestCase):
    def setUp(self):
        # Horario estandar

        global s1, s2, s3, h1, h2, h3, hm
        global csv_r,json_r,pp

        #  pp = pprint.PrettyPrinter()

        s1 = {
            "lun": ("07:00", "08:30"),
            "mar": ("07:00", "08:30"),
            "mie": ("07:00", "08:30"),
            "jue": ("07:00", "08:30"),
            "vie": ("07:00", "08:30"),
            "sab": ("07:00", "08:30"),
        }

        # Horario de 3 días a la semana (hay traslape con s1)

        s2 = {
            "lun": ("08:00", "10:00"),
            "mie": ("08:00", "10:00"),
            "jue": ("08:00", "10:00"),
            "vie": ("08:00", "10:00"),
        }

        # Horario de 2 días a la semana (hay traslape con s2 pero no con s1)

        s3 = {"mar": ("09:30", "12:00"), "jue": ("09:30", "12:00")}

        self.horario_instance = hs.HorarioClase()

        h1 = hs.HorarioClase(x="A")
        h2 = hs.HorarioClase(x="B")
        h3 = hs.HorarioClase(x="C")

        h1.set_prof("DRA. QUINTANA GUERRA MARIA ROSA")
        h2.set_prof("DRA. JIMENEZ MANCILLA NAYELI PATRICIA")
        h3.set_prof("M. EN C. TRUJILLO FLORES EDUARDO")

        h1.set_cve("C001")
        h2.set_cve("C451")
        h3.set_cve("L809")

        h1.set_num("23")
        h2.set_num("11")
        h3.set_num("45")


        h1.set_grid(s1)
        h2.set_grid(s2)
        h3.set_grid(s3)

        hm = hs.HorarioMaestro(titulo="Un horario")

        csv_r = lc.LectorPlantilla()
        csv_r.set_archivo(TEST_FILE)
        csv_r.instanciar_dict_reader()

        json_r = lc.LectorJSON()
        json_r.set_archivo(TEST_JSON)

    def test_time_delta(self):
        t_d = hs.time_delta("12:00", "11:00")
        self.assertEqual(t_d, 60)
        self.assertIsInstance(t_d, int)
        t_d = hs.time_delta("12:00", "11:30")
        self.assertEqual(t_d, 30)
        self.assertIsInstance(t_d, int)

    def test_set_grid(self):
        self.horario_instance.set_grid(s1)
        self.horario_instance.set_grid(s2)
        self.horario_instance.set_grid(s3)

    def test_horarios_compatibles(self):

        horarios_compatibles = hs.horarios_compatibles

        self.assertFalse(horarios_compatibles(h1, h2))
        self.assertTrue(horarios_compatibles(h1, h3))
        self.assertFalse(horarios_compatibles(h2, h3))

    def test_merge_grid(self):
        hm = hs.HorarioMaestro("Horario A")
        hm.merge(h1)
        hm.merge(h3)
        #  hm.display()

    def test_error(self):
        hs.error_out("Mensaje de prueba")

    def test_lector_csv(self):
        horario = csv_r.buscar_por_num("24")
        horario_maestro = hs.HorarioMaestro("Prueba de lectura csv")

        horario_maestro.merge(horario)

        horario_maestro.display()

    def test_lector_json(self):
        json_r.parse_json()
        self.assertEqual(json_r.lic,"ICO")
        self.assertEqual(json_r.num_cursar,0)
        self.assertEqual(json_r.semilla,"")

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
