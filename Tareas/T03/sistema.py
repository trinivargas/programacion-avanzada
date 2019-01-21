from estructuras import ListaLigada
from entidades import (Casa, Distribucion, Transmision, Elevadora)

class Sistema:
    def __init__(self, sigla):
        self.sigla = sigla # sigla del sigla electrico
        self.centrales = ListaLigada()
        self.elevadoras = ListaLigada()
        self.transmisiones = ListaLigada()
        self.distribuciones = ListaLigada()
        self.casas = ListaLigada()

    @property
    def potencia(self):
        potencia = 0
        for elevadora in self.elevadoras:
            potencia += elevadora.entidad.potencia
        return potencia

    @property
    def potencia_recibida(self):
        return

    def agregar_elevadora(self, elevadora):
        self.elevadoras.agregar(elevadora.id_, elevadora)

    def agregar_central(self, central):
        # solo si está permitido
        self.centrales.agregar(central.id_, central)

    def agregar_transmision(self, transmision):
        self.transmisiones.agregar(transmision.id_, transmision)

    def agregar_distribucion(self, distribucion):
        self.distribuciones.agregar(distribucion.id_, distribucion)

    def agregar_casa(self, casa):
        self.casas.agregar(casa.id_, casa)

    def eliminar_casa(self, id_):
        self.casas.eliminar(id_)

    def eliminar_distribucion(self, id_):
        self.distribuciones.eliminar(id_)

    def eliminar_nodos_sin_conexion(self):
        casas_a_eliminar = ListaLigada()
        for casa in self.casas:
            if not casa.entidad.conectado:
                casas_a_eliminar.agregar(casa.id_)
        for casa in casas_a_eliminar:
            self.casas.eliminar(casa.id_)
        distribuciones_a_eliminar = ListaLigada()
        for distribucion in self.distribuciones:
            if not distribucion.entidad.conectado:
                distribuciones_a_eliminar.agregar(distribucion.id_)
        for distribucion in distribuciones_a_eliminar:
            self.distribuciones.eliminar(distribucion.id_)
        transmisiones_eliminar = ListaLigada()
        for transmision in self.transmisiones:
            if not transmision.entidad.conectado:
                transmisiones_eliminar.agregar(transmision.id_)
        for transmision in transmisiones_eliminar:
            self.transmisiones.eliminar(transmision.id_)
        elevadoras_eliminar = ListaLigada()
        for elevadora in self.elevadoras:
            if not elevadora.entidad.conectado:
                elevadoras_eliminar.agregar(elevadora.id_)
        for elevadora in elevadoras_eliminar:
            self.elevadoras.eliminar(elevadora.id_)

    def potencia_real(self):
        self.borrar_potencia_ideal_y_real()
        p = 0
        for elevadora in self.elevadoras:
            elevadora.entidad.potencia_real()
            p += elevadora.entidad.p_real
        return p

    def borrar_potencia_ideal_y_real(self):
        for elevadora in self.elevadoras:
            elevadora.entidad.p_ideal = 0
            elevadora.entidad.p_real = 0
        for central in self.centrales:
            central.entidad.p_ideal = 0
            central.entidad.p_real = 0
        for transmision in self.transmisiones:
            transmision.entidad.p_ideal = 0
            transmision.entidad.p_real = 0
        for distribucion in self.distribuciones:
            distribucion.entidad.p_ideal = 0
            distribucion.entidad.p_real = 0
        for casa in self.casas:
            casa.entidad.p_ideal = 0
            casa.entidad.p_real = 0


