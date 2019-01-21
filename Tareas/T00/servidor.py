from datetime import datetime, timedelta
from random import randint
from clases import Usuario, Correo, Evento

class Servidor:
    def __init__(self):
        self.usuarios_servidor = dict()
        self.eventos = dict()
        self.usuario_activo = None # es una instancia de usuario
        self.cargar_db()
        self.inicio()

    def inicio(self):
        print('\nInicio DCCorreos \n(1) Iniciar sesión\n'
              '(2) Registrarse\n(0) Salir')
        accion = input('Opción: ')
        if accion == '1':
            self.usuario_activo = self.iniciar_sesion()
            self.menu()
        elif accion == '2':
            return self.registro()
        elif accion == '0':
            return
        self.inicio()

    def iniciar_sesion(self):
        nombre_usuario = input('Ingrese su nombre de usuario: ')
        if self.usuarios_servidor.get(nombre_usuario) == None:
            print('Este usuario no existe.')
            return self.iniciar_sesion()
        contrasena = input('Ingrese su contraseña: ')
        usuario = self.usuarios_servidor[nombre_usuario]
        if usuario.contrasena != contrasena:
            print('Su contraseña es inválida.')
            return self.iniciar_sesion()
        return usuario

    ############################   Correo   ###############################
    # Registrar nuevo correo
    def registro(self):
        direccion = input('Su usuario debe tener un nombre y direccion de '
                          'servicio válido. Además no puede tener (,) ni '
                          '(;)\nNombre de usuario: ')
        while not self.nombre_valido(direccion):
            direccion = input('Ingrese otro nombre de usuario: ')
        contrasena = input('Ingrese una contraseña de al menos 6 carácteres'
                           'y que no contenga (,) ni (;)\nContraseña: ')
        while not self.contrasena_valida(contrasena):
            contrasena = input('Ingrese una contraseña válida: ')
        self.usuarios_servidor[direccion] = Usuario(direccion, contrasena)
        with open('data/db_users.csv', 'a') as archivo:
            archivo.write(f'\n{direccion},{contrasena}')
        print(f'¡Felicitaciones! su cuenta de DCCorreos {direccion} '
              f'ha sido creada.')
        self.inicio()

    def nombre_valido(self, usuario):
        if usuario.count('@') != 1 or ',' in usuario or ';' in usuario:
            print('Este usuario no es válido.')
            return False
        nombre, direccion = usuario.split('@')
        if not '.' in direccion or nombre == '':
            print('Este usuario no es válido.')
            return False
        direccion = direccion.split('.')
        for e in direccion:
            if e == '':
                print('Este usuario no es válido.')
                return False
        if self.usuarios_servidor.get(usuario) != None:
            print('Este correo ya existe.')
            return False
        return True

    def contrasena_valida(self, contrasena):
        if len(contrasena) < 6 or ',' in contrasena or ';' in contrasena:
            return False
        return True

    ############################ Menu DCCorreos  #############################
    def menu(self):
        print(f'\nMenú DCCorreos - {self.usuario_activo.direccion}\n(1) Ban'
              f'deja de entrada\n(2) Enviar correo\n(3) Calendario\n(0) Salir')
        accion = input('Opción: ')
        if accion == '1':
            self.bandeja_entrada()
        elif accion == '2':
            self.crear_correo()
        elif accion == '3':
            self.calendario()
        elif accion == '0':
            return
        self.menu()

    # Bandeja de entrada
    def bandeja_entrada(self):
        print(f'\nBandeja de entrada DCCorreos')
        for i, correo in enumerate(self.usuario_activo.bandeja_entrada):
            print(f'{i + 1}.- {", ".join(correo.clasificacion)}   '
                  f'| {correo.asunto}')
        print('\nPara abrir un correo ingrese el número (n) y para salir (0)')
        opcion = input('Opción: ')
        largo = len(self.usuario_activo.bandeja_entrada)
        if opcion.isdigit() and 0 < int(opcion) <= largo:
            correo = self.usuario_activo.bandeja_entrada[int(opcion) - 1]
            self.abrir_correo(correo)
        if opcion == '0':
            return
        self.bandeja_entrada()

    def abrir_correo(self, correo):
        clasificacion = ', '.join(correo.clasificacion)
        print(f'\nDe: {correo.de}\nAsunto: {correo.asunto}\nClasificacion: '
              f'{clasificacion}\n{self.decodificar(correo.cuerpo)}')
        input('Volver ')

    # Enviar correo
    def crear_correo(self):
        de = self.usuario_activo.direccion #es un string
        destin = self.destinatarios() #lista con strings de los nombres
        asunto = self.asunto() #string
        cuerpo = self.cuerpo() #string de 0's 1's y cadena_aleatoria
        opciones = self.opciones() #lista
        clasificacion = " ,".join(opciones)
        print(f'\nDe: {de}\nPara: {", ".join(destin)}\nAsunto: {asunto}\n'
              f'Clasificación: {clasificacion}\n{self.decodificar(cuerpo)}\n')
        if self.confirmar():
            correo = Correo(de, destin, asunto, cuerpo, opciones)
            for dest in destin:
                self.usuarios_servidor[dest].bandeja_entrada.append(correo)
            with open('data/db_emails.csv', 'a', encoding ='utf-8') as file:
                file.write(f'\n{str(correo)}')
            print('El correo ha sido enviado con éxito.')
        else:
            print('Su correo no ha sido enviado.')

    def destinatarios(self):
        destin = input('Ingrese los destinatarios separados por (,)\nPara: ')
        destin = destin.split(',')
        destinatarios = []
        for dest in destin:
            if dest != '' :
                d = dest.strip()
                if d in self.usuarios_servidor and d not in destinatarios:
                    destinatarios.append(d)
        if len(destinatarios) == 0:
            print('Debe ingresar al menos un destinatario existente.')
            return self.destinatarios()
        return destinatarios

    def asunto(self):
        asunto = input('Ingrese un asunto no vacío y de máximo 50 caracteres\n'
                       'Asunto: ')
        if len(asunto) < 1 or len(asunto) > 50:
            print('El asunto no cumple el largo permitido.')
            return self.asunto()
        return asunto

    def cuerpo(self):
        cuerpo = input('Escriba el cuerpo de máximo 256 caracteres\nCuerpo: ')
        if not (0 < len(cuerpo) <= 256):
            print('El cuerpo no cumple con el largo permitido.')
            return self.cuerpo()
        cuerpo = self.codificar(cuerpo)
        return cuerpo

    def opciones(self):
        marcas = ['Importante', 'Publicidad', 'Destacado', 'Newsletter']
        seleccionado = []
        print('Clasificación del correo:\nSi tiene más de una clasificación '
              'separelos por una coma. Ej: (1,2)\n(1) {}\n(2) {}\n(3) {}\n'
              '(4) {}'.format(marcas[0], marcas[1], marcas[2], marcas[3]))
        opcion = input('Opción: ')
        opcion = opcion.split(',')
        for o in opcion:
            if o.strip() in ['1', '2', '3', '4']:
                seleccionado.append(marcas[int(o.strip())-1])
        if len(seleccionado) == 0:
            seleccionado.append('Sin clasificación')
        return seleccionado

    def confirmar(self):
        respuesta = input('(1) Enviar\n(2) Cancelar\nOpción: ')
        if respuesta == '1':
            return True
        elif respuesta == '2':
            return False
        return self.confirmar()

    ###########################    Calendario     ############################
    def calendario(self):
        usuario = self.usuario_activo
        print(f'\nCalendario de {usuario.direccion}')
        for evento in self.eventos.values():
            if usuario.direccion == evento.dueno or usuario.direccion in \
            evento.invitados:
                print(f'Evento {evento.ide}: {evento.nombre} Fecha: '
                      f'{evento.inicio} a {evento.termino}\nEtiquetas: '
                      f'{", ".join(evento.etiquetas)}')
        print('\nAcciones disponibles\n(0) Volver\n(1) Crear evento\n(2) '
              'Abrir evento\n(3) Buscar')
        opcion = input('Opción: ')
        if opcion == '0':
            return
        elif opcion == '1':
            self.nuevo_evento()
        elif opcion == '2':
            self.abrir_evento()
        elif opcion == '3':
            self.buscar()
        self.calendario()

    def buscar(self):
        print('Ingrese los criterios de búsqueda. Si no ingresa nada, '
              'no se considerará.')
        nombre = input('Nombre: ')
        etiqueta = input('Etiqueta: ')
        print('Ingrese las fechas de la forma Año-Mes-Día Hora:Minuto:Segundo')
        inicio = input('Fecha inicio: ')
        termino = input('Fecha termino: ')
        usuario = self.usuario_activo
        for e in self.eventos.values():
            if (usuario.direccion == e.dueno or usuario.direccion in
                e.invitados):
                if nombre != '' and etiqueta != '':
                    if (nombre in e.nombre and etiqueta in e.etiquetas):
                        print(f'Evento {e.ide}: {e.nombre} Fecha: '
                              f'{e.inicio} a {e.termino}\nEtiquetas: '
                              f'{", ".join(e.etiquetas)}')
                elif nombre == '' and etiqueta != '':
                    if etiqueta in e.etiquetas:
                        print(f'Evento {e.ide}: {e.nombre} Fecha: '
                              f'{e.inicio} a {e.termino}\nEtiquetas: '
                              f'{", ".join(e.etiquetas)}')
                elif nombre != '' and etiqueta == '':
                    if nombre in e.nombre:
                        print(f'Evento {e.ide}: {e.nombre} Fecha: '
                              f'{e.inicio} a {e.termino}\nEtiquetas: '
                              f'{", ".join(e.etiquetas)}')
        print('(1) Abrir evento\n(otro) Volver')
        opcion = input('Opción')
        if opcion == '1':
            self.abrir_evento()

    ###########################      Eventos   ###############################
    def nuevo_evento(self):
        evento = Evento()
        evento.crear(self.eventos, self.usuarios_servidor, self.usuario_activo)
        self.eventos[str(evento.ide)] = evento

    def abrir_evento(self):
        print('Escriba el número del evento que quiere abrir')
        numero = input('Número evento: ')
        if numero not in self.eventos:
            print('Este evento no existe.')
            return
        usuario = self.usuario_activo.direccion
        evento = self.eventos[numero]
        if not (usuario == evento.dueno or usuario in evento.invitados):
            print('Usted no tiene acceso a este evento.')
            return
        print(self.eventos[numero])
        print(f'(0) Volver\n(1) Editar evento')
        opcion = input('Opción: ')
        if opcion == '1':
            self.modificar_evento(self.eventos[numero])

    def modificar_evento(self, evento):
        if self.usuario_activo.direccion != evento.dueno:
            print('Solo el dueño del evento puede editarlo.')
            return
        print('\nOpciones:\n(0) Volver\n(1) Cambiar nombre\n(2) Cambiar fechas'
              '\n(3) Cambiar descripción\n(4) Agregar invitados\n(5) Agregar'
              ' etiquetas\n(6) Cambiar etiquetas\n(7) Eliminar')
        opcion = input('Opción: ')
        if opcion == '0':
            return
        elif opcion == '1':
            evento.nombre = evento.crear_nombre(self.eventos)
        elif opcion == '2':
            evento.cambiar_fechas()
        elif opcion == '3':
            evento.crear_descripcion() # si funciona :)
        elif opcion == '4':
            evento.invitar(self.usuarios_servidor)
        elif opcion == '5':
            evento.crear_etiquetas()
        elif opcion == '6':
            evento.etiquetas = ['Sin etiquetas']
            evento.crear_etiquetas()
        elif opcion == '7':
            del self.eventos[str(evento.ide)]
            print(f'Se ha eliminado el evento {evento.nombre}.')
        if opcion in ['1', '2', '3', '4', '5', '6', '7']:
            with open('data/db_events.csv', 'w', encoding = 'utf-8') as file:
                file.write('owner,name,start,finish,description,invited,tags')
                for e in self.eventos.values():
                    invitados = ';'.join(e.invitados)
                    etiquetas = ';'.join(e.etiquetas)
                    file.write(f"\n{e.dueno},'{e.nombre}',{e.inicio},"
                               f"{e.termino},'{e.descripcion}',{invitados},"
                               f"{etiquetas}")
            if opcion == '7':
                return
        self.modificar_evento(evento)

    ############################   Codificación   ############################
    def codificar(self, texto):
        clave = '2233'
        cadena_aleatoria = '' # Paso 3
        for i in range(10):
            cadena_aleatoria += str(randint(0, 9))
        cadena_inicio = (19 * (clave + cadena_aleatoria))[:256] # Paso 4
        lista = list(range(0, 256)) # Paso 5
        for i in range(256):
            j = i + int(cadena_inicio[i])
            if j > 255:
                j = j - 256
            lista_i = lista[i]
            lista_j = lista[j]
            lista[i] = lista_j
            lista[j] = lista_i
        cadena_a = '' # Paso 2 / 6a
        for letra in texto:
            codigo = bin(ord(letra) + 10)[2:]
            cadena_a += (8 - len(codigo)) * '0' + codigo
        cadena_b = '' # Paso 6b
        for numero in lista:
            codigo = bin(numero)[2:]
            cadena_b += (8 - len(codigo)) * '0' + codigo
        mensaje_codificado = '' # PAso 6c
        for i in range(len(cadena_a)):
            if cadena_a[i] == cadena_b[i]:
                mensaje_codificado += '0'
            else:
                mensaje_codificado += '1'
        return cadena_aleatoria + mensaje_codificado # Paso 7

    def decodificar(self, codigo):
        clave = '2233'
        cadena_aleatoria = codigo[:10]
        mensaje_codificado = codigo[10:]
        cadena_inicio = (19 * (clave + cadena_aleatoria))[:256]  # Paso 4
        lista = list(range(0, 256))  # Paso 5
        for i in range(256):
            j = i + int(cadena_inicio[i])
            if j > 255:
                j = j - 256
            lista_i = lista[i]
            lista_j = lista[j]
            lista[i] = lista_j
            lista[j] = lista_i
        cadena_b = '' #La cadena de la lista
        for numero in lista:
            codigo = bin(numero)[2:]
            cadena_b += (8 - len(codigo)) * '0' + codigo
        cadena_a = ''
        for i in range(len(mensaje_codificado)):
            b = cadena_b[i]
            if mensaje_codificado[i] == '0':
                cadena_a += b
            else:
                if b == '1':
                    cadena_a += '0'
                elif b == '0':
                    cadena_a += '1'
        mensaje = ''
        for i in range(0,len(cadena_a),8):
            mensaje += chr(int(cadena_a[i: i + 8], 2) - 10)
        return mensaje


    ############################   Cargar datos   ############################
    def cargar_db(self):
        with open('data/db_users.csv', 'r', encoding ='utf-8') as archivo:
            archivo.readline()
            for linea in archivo:
                usuario, contrasena = linea.split(',')
                self.usuarios_servidor[usuario] = Usuario(usuario,
                                                          contrasena.strip())
        with open('data/db_emails.csv', 'r', encoding ='utf-8') as archivo:
            archivo.readline()
            for linea in archivo:
                info = linea.split(',') # El asunto puede tener comas
                de, para, opciones = info[0], info[1], info[-1].strip()
                asunto, cuerpo = ','.join(info[2:-2])[1:-1], info[-2]
                destinatarios, opciones = para.split(';'), opciones.split(';')
                correo = Correo(de, destinatarios, asunto, cuerpo, opciones)
                for dest in destinatarios:
                    self.usuarios_servidor[dest].bandeja_entrada.append(correo)

        with open('data/db_events.csv', 'r', encoding ='utf-8') as archivo:
            archivo.readline()
            for line in archivo:
                if line != '\n' and line != '' and line.count(' ') != len(line):
                    info = line.split(',')
                    evento = Evento()
                    evento.dueno, evento.nombre = info[0], (info[1])[1:-1]
                    dia, hora = info[2].split(' ')
                    datos = dia.split('-') + (hora.split(':'))
                    evento.inicio = datetime(*map(lambda num: int(num), datos))
                    dia, hora = info[3].split(' ')
                    datos = dia.split('-') + (hora.split(':'))
                    evento.termino = datetime(*map(lambda num: int(num), datos))
                    evento.descripcion = ','.join(info[4:-2]).strip("'")
                    evento.invitados = info[-2].split(';')
                    evento.etiquetas = info[-1].strip().split(';')
                    self.eventos[str(evento.ide)] = evento

