"""
server.py -- un simple servidor
"""

import pickle
from socket import socket
import os # usar listdir

HOST = '127.0.0.1'


class Server:
    """
    Una clase que representa un servidor.
    """

    def __init__(self, port):
        self.host = HOST
        self.port = port
        self.client = None
        self.socket = socket()

        self.commands = {
            "ls": self.list_filenames,
            "download": self.send_file,
            "upload": self.save_file,
            "logout": self.disconnect,
        }

    def run(self):
        """
        Enciende el servidor que puede conectarse
        y recibir comandos desde un único cliente.
        """

        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Escuchando en {self.host}:{self.port}.")

        while self.client is None:
            self.client, _ = self.socket.accept()
            print("¡Un cliente se ha conectado!")

            while self.client:
                command, args = pickle.loads(self.receive())
                # recibe el nombre de la función y los argumentos como tupla?
                # command es un str y args una lista
                self.commands[command](*args)

        print("Arrivederci.")

    def send(self, message):
        """
        [COMPLETAR]
        Envía datos binarios al cliente conectado por el socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """

        stringified_value = str(message)
        msg_bytes = stringified_value.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder='big')
        self.send(msg_length + msg_bytes)

    def receive(self):
        """
        [MODIFICAR]
        Recibe datos binarios del cliente, a través del socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """

        #return self.client.recv(128)  # maldición, esto es poco.

        response_bytes_length = self.client.recv(4)
        response_length = int.from_bytes(response_bytes_length, byteorder='big')
        response = bytearray()

        while len(response) < response_length:
            read_length = min(4096, response_length - len(response))
            response.extend(self.client.recv(read_length))

        return response # pickle.loads(response)

    def list_filenames(self):
        """
        [COMPLETAR]
        Envía al cliente una lista que contiene los nombres de
        todos los archivos existentes en la carpeta del servidor.
        """
        file_names = os.listdir(os.curdir)
        list_to_send = pickle.dumps(file_names)
        self.send(list_to_send)

    def send_file(self, filename):
        """
        [COMPLETAR]
        Envía al cliente un archivo ubicado en el directorio del servidor.
        """
        if filename not in os.listdir(os.curdir):
            self.send(pickle.dumps(None))

        else:
            with open(filename, 'br') as file:
                self.send(file)


    def save_file(self, filename):
        """
        [COMPLETAR]
        Guarda un archivo recibido desde el cliente.
        """

        # con el nombre del archivo se pide el archivo
        new_file = self.receive()
        with open(filename, 'bw', encoding='utf-8') as file:
            file.write(newfile)

    def disconnect(self):
        self.client = None
        print("El cliente se ha desconectado.")


if __name__ == '__main__':
    port_ = input("Escriba el puerto: ")
    server = Server(int(port_))
    server.run()
