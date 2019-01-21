"""
client.py -- un simple cliente
"""

import pickle
from socket import socket, SHUT_RDWR

HOST = '127.0.0.1'


class Client:
    """
    Una clase que representa un cliente.
    """

    def __init__(self, port):
        self.host = HOST
        self.port = port
        self.socket = socket()
        self.connected = False

        # Este diccionario tiene los comandos disponibles.
        # Puedes modificarlo para agregar nuevos comandos.
        self.commands = {
            "help": self.help,
            "logout": self.logout,
            "ls": self.ls,
            "upload": self.upload,
            "download": self.download
        }

    def run(self):
        """
        Enciende el cliente que puede conectarse
        para enviar algunos comandos al servidor.
        """

        self.socket.connect((self.host, self.port))
        self.connected = True

        while self.connected:
            command, *args = input('$ ').split()
            function = self.commands.get(command)

            if function is None:
                print(f"El comando '{command}' no existe.")
                print("Escribe 'help' para obtener ayuda.")
            elif command == 'help':
                self.help()
            else:
                self.send(pickle.dumps((command, args)))
                function(*args)

    def send(self, message):
        """
        [MODIFICAR]
        Envía datos binarios al servidor conectado por el socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """
        # supongo que message está en bytes. Para eso, cada función tiene que
        # convertir los datos a str
        largo_archivo = len(message)
        # no se si es sock o client o server // solo existe self.socket
        self.socket.sendall(largo_archivo.to_bytes(4, byteorder='big'))
        self.socket.sendall(message)


        self.socket.sendall(message)

    def receive(self):
        """
        [COMPLETAR]
        Recibe datos binarios del servidor, a través del socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """
        largo_archivo = int.from_bytes(self.socket.recv(4), byteorder='big')
        datos = bytearray()

        while len(datos) < largo_archivo:
            # El último recv será probablemente más chico que 4096
            bytes_leer = min(4096, largo_archivo - len(datos))
            datos_recibidos = sock_cliente.recv(bytes_leer)
            datos.extend(datos_recibidos)

        return pickle.loads(datos)

    def help(self):
        print("Esta es la lista de todos los comandos disponibles.")
        print('\n'.join(f"- {command}" for command in self.commands))

    def ls(self):
        """
        [COMPLETAR]
        Este comando recibe una lista con los archivos del servidor.

        Ejemplo:
        $ ls
        - doggo.jpg
        - server.py
        """
        # primero hay que llamar al servidor para que sepa que mandar
        #serealizado = pickle.dumps('ls')
        #self.send(serealizado)

        # necesito recibir los datos // la lista
        files = self.receive()
        files = pickle.loads(files)
        for file in files:
            print(f'- {file}')

    def upload(self, filename):
        """
        [COMPLETAR]
        Este comando envía un archivo hacia el servidor.
        manda el archivo o el nombre
        """

        #send_info = ['upload', filename] # en volá tiene que ser en lista [filename]
        #serealizado = pickle.dumps(send_info) # no se si es el archivo o el nombre
        #self.send(serealizado)

        # ahora hay que mandar el archivo
        with open(filename, 'br') as file:
            self.send(file_to_send)

        file_to_send = pickle.dumps(file_string)
        self.send(file_to_send)

    def download(self, filename):
        """
        [COMPLETAR]
        Este comando recibe un archivo ubicado en el servidor.
        El cliente entrega el nombre de un archivo del directorio del servidor
        y el servidor lo envía. Luego, el cliente lo guarda en su directorio.
        """
        #send_info = ['download', filename]
        #serealizado = pickle.dumps(send_info)

        file_info = self.receive()
        if pickle.loads(file_info) is None:
            print('Este archivo no existe!')

        with open(filename, 'bw', encoding='utf-8') as file:
            file.write(file_info)


    def logout(self):
        self.connected = False
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()
        print("Arrivederci.")


if __name__ == '__main__':
    port_ = input("Escriba el puerto: ")
    client = Client(int(port_))
    client.run()
