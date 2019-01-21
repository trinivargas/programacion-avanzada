from errores import InvalidQuery, ForbidenAction
from entidades import Distribucion, Transmision
ρ = 0.0172

class Consultas:
    def __init__(self, principal, red):
        self.principal = principal
        self.red = red
        self.p_total = 0

    def menu(self):
        opcion = '-1'
        self.red.eliminar_nodos_sin_conexion()
        self.p_total = self.red.potencia_real_red()
        while opcion != '0':
            print('\nConsultas:\n(1) Energía total consumida en una comuna\n(2) '
                  'Cliente con mayor consumo\n(3) Cliente con menor consumo\n'
                  '(4) Potencia perdida en transmision\n'
                  '(5) Consumo de una subestacion\n(0) Volver')
            opcion = self.principal.opcion(0, 5)
            if opcion == '1':
                self.consulta_energia_total_comuna()
            elif opcion == '2':
                self.consulta_cliente_mayor_consumo()
            elif opcion == '3':
                self.consulta_cliente_menor_consumo()
            elif opcion == '4':
                self.consulta_potencia_perdida()
            elif opcion == '5':
                self.consulta_consumo_subestacion()

    def consulta_energia_total_comuna(self):
        comuna = input('Comuna: ').upper()
        try:
            resultado = self._consulta_energia_total_comuna(comuna)
        except InvalidQuery as err:
            print(err, err.razon)
            resultado = self.consulta_energia_total_comuna()
        return resultado

    def _consulta_energia_total_comuna(self, comuna):
        self.p_total = self.red.potencia_real_red()
        distribuciones_comuna = self.distribuciones_comuna(comuna)
        p_comuna = 0
        for distribucion in distribuciones_comuna:
            p_comuna += distribucion.entidad.p_real
        print(f'Consumo comuna {comuna}: {round(p_comuna * 1000,3)} kW')
        if self.p_total:
            print(f'Consumo relativo: '
                  f'{round(p_comuna * 100 / self.p_total, 3)} %')
            return round(p_comuna * 1000, 3)
        print('La energía de la Red es 0 por lo que no se puede comparar.')

    def distribuciones_comuna(self, comuna):
        distribuciones = self.red.distribuciones_comuna(comuna)
        if distribuciones is None:
            raise InvalidQuery(f'No existe la comuna {comuna}')
        return distribuciones

    def consulta_cliente_mayor_consumo(self):
        sistema = self.pedir_sistema()
        mayor = self._consulta_cliente_mayor_consumo(sistema)
        if mayor is None:
            print('Ninguna casa tiene un consumo mayor a 0 kW')
            return mayor
        print(f'Casa con consumo máximo: Casa {mayor.id_}; Sitema '
              f'electrico: {mayor.sistema}; provincia: {mayor.provincia}; '
              f'comuna: {mayor.comuna}\nConsumo: '
              f'{round(mayor.p_real * 1000, 3)} kW')
        return mayor

    def _consulta_cliente_mayor_consumo(self, sistema):
        self.red.potencia_real_red()
        #sistema.potencia_real()
        consumo_maximo = 0
        mayor = None
        for casa in sistema.casas:
            if casa.entidad.p_real > consumo_maximo:
                mayor = casa.entidad
                consumo_maximo = casa.entidad.p_real
        return mayor

    def consulta_cliente_menor_consumo(self):
        sistema = self.pedir_sistema()
        menor = self._consulta_cliente_menor_consumo(sistema)
        if menor is None:
            print('No hay casas en el sistema')
            return
        print(f'Casa con consumo mínimo: Casa {menor.id_} Sistema electrico: '
              f'{menor.sistema}, Provincia: {menor.provincia} '
              f'Comuna: {menor.comuna}\nConsumo: {menor.p_real * 1000} kW')
        return menor

    def _consulta_cliente_menor_consumo(self, sistema):
        self.red.potencia_real_red()
        #sistema.potencia_real()
        menor = None
        consumo_minimo = 31  # ninguna casa pued tener más de 30 MW
        for casa in sistema.casas:
            if casa.entidad.conectado and casa.entidad.p_real < consumo_minimo:
                menor = casa.entidad
                consumo_minimo = casa.entidad.p_real
        return menor

    def pedir_sistema(self):
        try:
            sistema = self._pedir_sistema()
        except InvalidQuery as err:
            print(err, err.razon)
            sistema = self.pedir_sistema()
        return sistema

    def _pedir_sistema(self):
        sigla = input('Ingrese la sigla del sistema electrico: ').upper()
        sistema = self.red.encontrar_sistema(sigla)
        if sistema is None:
            raise InvalidQuery(f'No existe el sistema con sigla {sigla}')
        return sistema

    def consulta_potencia_perdida(self):
        casa = self.pedir_casa()
        resultado =  self._consultas_potencia_perdidas(casa)
        print(f'La potencia total perdida es de {resultado * 1000} kW')
        return resultado

    def pedir_casa(self):
        try:
            casa = self._pedir_casa()
        except InvalidQuery as err:
            print(err)
            casa = self.pedir_casa()
        return casa

    def _pedir_casa(self):
        id_ = input('id casa: ')
        if not id_.isdigit():
            raise InvalidQuery('No es un id válido')
        casa = self.red.casas[id_]
        if casa is None:
            raise InvalidQuery('Casa no existe')
        return casa

    def _consultas_potencia_perdidas(self, casa):
        self.red.potencia_real_red()
        perdida = 0
        sistema = self.red.encontrar_sistema(casa.sistema)
        # suma la potencia de las distribuciones a la casa
        distribuciones_comuna = self.distribuciones_comuna(casa.comuna)
        for distribucion in distribuciones_comuna:
            camino = distribucion.entidad.nodos_hijos(casa.id_)
            perdida += self.calcular_perdida_distribucion_casa(camino)
            for transmision in sistema.transmisiones:
                for distribucion_t in transmision.entidad.conexiones:
                    if distribucion_t.id_ == distribucion.id_:
                        trans = transmision.entidad
                        dist = distribucion_t.entidad
                        resistencia = ρ * distribucion_t.distancia / 152
                        manda = dist.p_real / (1 - resistencia)
                        perdida += manda - dist.p_real
        for elevadora in sistema.elevadoras:
            for conexion in elevadora.entidad.conexiones:
                if conexion.id_ == trans.id_:
                    trans = conexion.entidad
                    resistencia = ρ * conexion.distancia / 202.7
                    manda = trans.p_real / (1 - resistencia)
                    perdida += manda - trans.p_real
        return round(perdida, 6)

    def calcular_perdida_distribucion_casa(self, camino):
        perdida = 0
        for nodo in camino:
            if nodo.siguiente is not None:
                conexiones = nodo.entidad.conexiones
                for conexion in conexiones:
                    if conexion.id_ == nodo.siguiente.id_:
                        casa = nodo.siguiente.entidad
                        resistencia = ρ * conexion.distancia / 85
                        manda = (casa.p_real /casa.conectado) /(1 - resistencia)
                        perdida += manda - nodo.siguiente.entidad.p_real
                        print(manda - nodo.siguiente.entidad.p_real)
        return perdida


    def consulta_consumo_subestacion(self):
        tipo = self.pedir_tipo_estacion()
        estacion = self.pedir_estacion(tipo)
        resultado = self._consulta_consumo_subestacion(estacion)
        print(f'Consumo total: {resultado} MW')
        return resultado

    def _consulta_consumo_subestacion(self, estacion):
        self.red.potencia_real_red()
        if not (isinstance(estacion, Distribucion) or isinstance(estacion, Transmision)):
            raise ForbidenAction()
        self.red.encontrar_sistema(estacion.sistema).potencia_real()
        estacion.potencia_real()
        return round(estacion.p_real, 3)

    def pedir_tipo_estacion(self):
        print('¿Qué tipo de estación quiere buscar?\n'
              '(1) Subestación Transmisión\n(2) Subestación Distribución')
        opcion = self.principal.opcion(1, 2)
        if opcion == '1':
            return 'transmision'
        return 'distribucion'

    def pedir_estacion(self, tipo):
        try:
            estacion = self._pedir_estacion(tipo)
        except InvalidQuery as err:
            print(err, err.razon)
            estacion = self.pedir_estacion(tipo)
        return estacion

    def _pedir_estacion(self, tipo):
        id_ = input('Ingrese el id de la subestación: ')
        if tipo == 'distribucion':
            estacion = self.red.distribuciones[id_]
        else:
            estacion = self.red.transmisiones[id_]
        if estacion is None:
            raise InvalidQuery(f'No existe ninguna subestación de {tipo} '
                               f'con id {id_}')
        return estacion


