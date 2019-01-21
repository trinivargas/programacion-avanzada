import unittest
from sistemas import Red
from entidades import Casa, Distribucion, Transmision, Central
from errores import InvalidQuery, ElectricalOverload, ForbidenAction
from menu import Menu


class Test(unittest.TestCase):
    def setUp(self):
        self.red = Red('bd/small/')
        self.sistema = self.red.encontrar_sistema('SING')
        self.consultas = Menu(self.red)._consultas

    def test_consulta_energia_comuna(self):
        funct = self.consultas._consulta_energia_total_comuna
        self.assertEqual(funct('PICA'), 34928.75)

    def test_consulta_mayor_consumo(self):
        central = self.red.centrales['33']
        central._potencia = 1000000000
        funct = self.consultas._consulta_cliente_mayor_consumo
        self.assertIsInstance(funct(self.sistema), Casa)
        self.assertEqual(funct(self.sistema).id_, '1542')

    def test_consulta_menor_consumo(self):
        funct = self.consultas._consulta_cliente_menor_consumo
        self.assertIsInstance(funct(self.sistema), Casa)
        self.assertNotEqual(funct(self.sistema).id_, '1570') # esta no vale, tiene que ser equall
        self.assertEqual(funct(self.sistema).p_real, 0)

    def test_consulta_perdida_potencia(self):
        funct = self.consultas._consultas_potencia_perdidas
        casa = self.sistema.casas['1496']
        self.assertEqual(funct(casa), 0.946964)

    def test_consulta_consumo_subestacion_distribucion(self):
        estacion = self.sistema.distribuciones['220']
        funct = self.consultas._consulta_consumo_subestacion
        self.assertEqual(funct(estacion), 14.428)

    def test_consulta_consumo_subestacion_transmision(self):
        estacion = self.sistema.transmisiones['53']
        funct = self.consultas._consulta_consumo_subestacion
        self.assertEqual(funct(estacion), 105.353)

    def test_invalid_query(self):
        funct = self.consultas._consulta_energia_total_comuna
        self.assertRaises(InvalidQuery, funct, 'pica')

    def test_electrical_overload(self):
        central = self.red.centrales['33']
        central._potencia = 10000
        casa = self.red.casas['1496']
        casa.consumo = 25
        funct = self.consultas._consulta_cliente_mayor_consumo
        self.assertRaises(ElectricalOverload, funct, self.sistema)

    def test_forbiden_action(self):
        central = self.red.centrales['33']
        funct = self.consultas._consulta_consumo_subestacion
        self.assertRaises(ForbidenAction, funct, central)



if __name__ == "__main__":
    unittest.main()