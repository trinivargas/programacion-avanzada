from itertools import count

class Persona:
    _id = count(start=0)
    # el id_ es único para cada persona (no se repite entre cliente y personal)
    def __init__(self, nombre, edad, *args):
        super().__init__(*args)
        self.nombre = nombre
        self.edad = edad
        self._id = next(Persona._id)
        self.actividad = None
        self.tiempo_restante_actividad = 0

    @property
    def ocupado(self):
        return self.actividad is not None

    def desocupar(self):
        self.actividad = None
        self.tiempo_restante_actividad = 0