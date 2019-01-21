import unittest
from dccontrolador import Supermercado, Producto, PedidoOnline, \
    RepeatedError, InconsistencyError

###############################################################################
"""
Tests
Acá escribe los test pedidos.
"""

class Test(unittest.TestCase):
    def setUp(self):
        


    def test_invalid_caracters(self):
        self.assertRaises(ValueError, supermercado.agregar_producto, 'hola@', 'producto')

    def test_precio_cero(self):
        self.assertEqual(PedidoOnline.)



###############################################################################

if __name__ == '__main__':
    unittest.main()
