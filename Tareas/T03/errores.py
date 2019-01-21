class ElectricalOverload(Exception):
    def __init__(self, potencia):
        super().__init__('ElectricalOverload:')
        self.potencia = potencia


class ForbidenAction(Exception):
    def __init__(self, msg='', accion=None, porque=None):
        self.accion = accion
        self.razon = porque
        super().__init__('ForbidenAction:' + msg)


class InvalidQuery(Exception):
    def __init__(self, razon=None):
        self.razon = razon
        super().__init__('InvalidQuery:')

