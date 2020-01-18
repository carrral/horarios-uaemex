import unittest
from horarios import horarios as hs


class HorariosTest(unittest.TestCase):
    def setUp(self):
        # Horario estandar

        global s1, s2, s3
        s1 = {
            "lun": ("0700", "0830"),
            "mar": ("0700", "0830"),
            "mie": ("0700", "0830"),
            "jue": ("0700", "0830"),
            "vie": ("0700", "0830"),
            "sab": ("0700", "0830"),
        }

        # Horario de 3 días a la semana (hay traslape con s1)

        s2 = {"lun": ("0800", "1000"), "mie": ("0800", "1000"), "vie": ("0800", "1000")}

        # Horario de 2 días a la semana (hay traslape con s2 pero no con s1)

        s3 = {"mar": ("0930", "1200"), "jue": ("0930", "1200")}

        self.horario_instance = hs.Horario()

    def test_time_delta(self):
        t_d = hs.time_delta("1200", "1100")
        self.assertEqual(t_d, 60)
        self.assertIsInstance(t_d, int)
        t_d = hs.time_delta("1200", "1130")
        self.assertEqual(t_d, 30)
        self.assertIsInstance(t_d, int)

    def test_get_grid(self):
        self.horario_instance.set_grid(s1)

    def test_print_grid(self):
        self.horario_instance.set_grid(s1)
        hs.print_grid(self.horario_instance.grid)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
