from datetime import datetime, timedelta

class Correo:
    def __init__(self,de, destinatarios, asunto, cuerpo, clasificacion):
        self.de = de # direccion
        self.destinatarios = destinatarios
        self.asunto = asunto
        self.cuerpo = cuerpo
        self.clasificacion = clasificacion

    def __str__(self):
        return f"{self.de},{';'.join(self.destinatarios)},'{self.asunto}'," \
               f"{self.cuerpo},{';'.join(self.clasificacion)}"


class Usuario:
    def __init__(self, direccion, contrasena):
        self.direccion = direccion
        self.contrasena = contrasena
        self.bandeja_entrada = []
        self.eventos_propios = []
        self.eventos_invitados = []


class Evento:
    id_ = 0

    def __init__(self):
        Evento.id_ += 1
        self.ide = Evento.id_
        self.dueno = None
        self.nombre = ''
        self.inicio = None
        self.termino = None
        self.descripcion = 'Sin descripción'
        self.invitados = ['Sin invitados']
        self.etiquetas = ['Sin etiquetas']

    def crear(self, eventos, usuarios, dueno):
        self.dueno = dueno.direccion  # tiene que ser un string
        self.nombre = self.crear_nombre(eventos)
        print('Ingrese las fechas en la forma Año-Mes-Dia Hora:Minuto:Segundo')
        self.inicio = self.fecha_inicio(eventos)
        self.termino = self.fecha_termino(eventos)
        self.crear_descripcion()
        self.invitar(usuarios)
        self.crear_etiquetas()
        invitados = ';'.join(self.invitados)
        etiquetas = ';'.join(self.etiquetas)
        with open('data/db_events.csv', 'a', encoding = 'utf-8') as file:
            file.write(f'\n{self.dueno},{self.nombre},{self.inicio},')
            file.write(f'{self.termino},{self.descripcion},{invitados},')
            file.write(f'{etiquetas}')
        print('¡Su evento ha sido creado con exito!')

    def crear_nombre(self, eventos):
        print('Ingrese un nombre entre 6 y 50 caracteres')
        nombre = input('Nombre: ')
        while len(nombre) < 6 or len(nombre) > 50 or nombre in eventos:
            print('El nombre no es válido o ya existe.')
            nombre = input('Nombre: ')
        return nombre

    def fecha_inicio(self, eventos):
        fecha = input('Fecha inicio: ')
        fecha_valida = self.fecha_valida(fecha)
        while not (fecha_valida and self.fecha_libre(eventos, fecha_valida)):
            fecha = input('Fecha de inicio: ')
            fecha_valida = self.fecha_valida(fecha)
        return fecha_valida  # retorna fecha de tipo datetime

    def fecha_termino(self, eventos): # para no poner fecha no poner nada
        fecha = input('Fecha de término: ')
        if fecha == '':
            fecha_valida = self.inicio + timedelta(hours = 1)
            print(f'Por defecto la fecha de término es {fecha_valida}')
        else:
            fecha_valida = self.fecha_valida(fecha)
        while not (fecha_valida and self.fecha_libre(eventos, fecha_valida)
                   and self.fecha_posterior(fecha_valida)):
            fecha = input('Fecha de término: ')
            if fecha == '':
                fecha_valida = self.inicio + timedelta(hours = 1)
            else:
                fecha_valida = self.fecha_valida(fecha)
        return fecha_valida

    def fecha_valida(self, fecha):  # Existe la fecha.
        if (fecha.count(' ') != 1 or fecha.count('-') != 2
            or fecha.count(':') != 2):
            print('La fecha ingresada no cumple con el formato correcto')
            return False
        dia, hora = fecha.split(' ')
        fecha = dia.split('-') + hora.split(':')
        valido = map(lambda s: s.isdigit(), fecha)
        if False in valido:
            return False
        f = tuple(map(lambda num: int(num), fecha))
        dias_mes = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        if not (0 < f[0] < 10000 and 0 < f[1] < 13
                and 0 < f[2] <= dias_mes[f[1] - 1] and 0 <= f[3] < 24
                and 0 <= f[4] < 60 and 0 <= f[5] < 60):
            print('Esta fecha no existe.')
            return False
        return datetime(*f)

    def fecha_libre(self, eventos, fecha):  # fecha de tipo datetime
        for evento in eventos.values():
            inicio, termino = evento.inicio, evento.termino
            if inicio <= fecha <= termino:
                print('Esta fecha ya está ocupada.')
                return False
        return fecha

    def fecha_posterior(self, termino):
        if not (self.inicio < termino):
            print('La fecha de término no puede ser antes de la de inicio.')
            return False
        return True

    def crear_descripcion(self):
        print('Agregue una descripción. Si no agrega nada será Sin descripción')
        descripcion = input('Descripción: ')
        if descripcion == '' or descripcion.count(' ') == len(descripcion):
            self.descripcion =  'Sin descripción'
            return
        self.descripcion = descripcion

    def invitar(self, usuarios):
        print('Agregue los invitados separados por (,).')
        invitados = input('Invitados: ')
        invitados = invitados.split(',')
        inv_agregados = []
        for inv in invitados:
            if (inv != '' and inv.count(' ') != len(inv)
                and inv.strip() in usuarios and inv.strip() not in inv_agregados
                    and inv.strip() not in self.invitados):
                inv_agregados.append(inv.strip())
        if len(inv_agregados) > 0 and ('Sin invitados' in self.invitados
                                       or 'sin invitados' in self.invitados):
            self.invitados = inv_agregados
            return
        elif len(inv_agregados) > 0:
            self.invitados.extend(inv_agregados)
            return


    def crear_etiquetas(self):
        print('Agregue etiquetas separadas por (,).')
        etiquetas = input('Etiquetas: ')
        nuevas_etiquetas = []
        etiquetas = etiquetas.split(',')
        for etiqueta in etiquetas:
            if etiqueta != '' and etiqueta.count(' ') != len(etiqueta):
                nuevas_etiquetas.append(etiqueta.strip())
        if len(nuevas_etiquetas) > 0 and ('Sin etiquetas' in self.etiquetas
                                          or 'sin etiquetas' in self.etiquetas):
            self.etiquetas = nuevas_etiquetas
            return
        elif len(nuevas_etiquetas) > 0:
            self.etiquetas.extend(nuevas_etiquetas)
            return

    def cambiar_fechas(self):
        print('Ingrese las fechas de la forma Año-Mes-Día Hora:Minuto:Segundo')
        inicio = input('Fecha de inicio: ')
        while not self.fecha_valida(inicio):
            inicio = input('Fecha de inicio: ')
        self.inicio = self.fecha_valida(inicio)
        termino = input('Fecha de término: ')
        if termino == '' or termino.count(' ') == len(termino):
            self.termino = self.inicio + timedelta(hours = 1)
            print(f'Por defecto la fecha de término es {self.termino}')
            return
        while not self.fecha_valida(termino) and self.fecha_posterior(termino):
            termino = input('Fecha de término: ')
            if termino == '' or termino.count(' ') == len(termino):
                self.termino = self.inicio + timedelta(hours = 1)
                print(f'Por defecto la fecha de término es {self.termino}')
                return

    def __str__(self):
        return f'\nEvento {self.ide}: {self.nombre}\nDueño: {self.dueno}\nFe' \
               f'cha: {self.inicio} a {self.termino}\nDescripción: ' \
               f'{self.descripcion}\nInvitados: {", ".join(self.invitados)}\n' \
               f'Etiquetas: {", ".join(self.etiquetas)}'
