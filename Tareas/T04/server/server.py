import threading as th
import socket
import json
import pickle
from os import urandom
from hashlib import sha256

from waiting_room import WaitingRoom
from game import Game

# código sacado de la ayudantia de este semestre

HOST = "localhost"
PORT = 8081

class Server:

    global_lock = th.Lock()

    def __init__(self):
        self.host = HOST
        self.port = PORT

        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}... ")

        thread = th.Thread(target=self.accept_connections_thread, daemon=True)
        thread.start()
        print("Servidor aceptando conexiones...")

        # estructuras para el juego
        self.load_server_users()
        self.users = set()
        self.sockets = dict()
        self.clients = dict()
        self.waiting_room = WaitingRoom()
        self.games = dict()
        self.number_waiting_rooms = 0
        self.number_games = 0
        self.clients_game = dict()
        self.player_number = dict()


    def accept_connections_thread(self):
        '''
        Este método es utilizado en el thread para ir aceptando conexiones de
        manera asíncrona al programa principal
        :return:
        '''

        while True:
            client_socket, _ = self.socket_servidor.accept() # _ es adress
            self.sockets[client_socket] = None
            print("Servidor conectado a un nuevo cliente...")

            listening_client_thread = th.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()
            self.clients[client_socket] = {'status': 'not logged in',
                                           'username': None, 'game': None,
                                           'chief': None, 'score': None,
                                           'color': None,
                                           'waiting room info': None,
                                           'n': None}

            if len(self.sockets) == 5: # si no permite más conecciones
                break

    def listen_client_thread(self, client_socket):
        '''
        Este método va a ser usado múltiples veces en threads pero cada vez con
        sockets de clientes distintos.
        :param client_socket: objeto socket correspondiente a algún cliente
        '''

        while True:
            try:
                response_bytes_length = client_socket.recv(4)
                response_length = int.from_bytes(response_bytes_length,
                                                 byteorder="big")

                response = bytearray()

                while len(response) < response_length:
                    response += client_socket.recv(256)

                response = response.decode()
                decoded = json.loads(response)

                # handle command
                self.handle_command(decoded, client_socket)

            except ConnectionResetError:
                decoded_message = {"status": "cerrar_sesion"}
                self.handle_command(decoded_message, client_socket)
                break

    @staticmethod
    def send(value, socket):
        '''
        Este método envía la información al cliente correspondiente al socket.
        :param msg: dict del tipo {"status": tipo del mensaje, "data": info}
        :param socket: socket del cliente al cual se le enviará el mensaje
        '''
        msg_json = json.dumps(value)
        msg_bytes = msg_json.encode()

        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")

        socket.send(msg_length + msg_bytes)

    def handle_command(self, received, client_socket):
        '''
        Este método toma lo recibido por el cliente correspondiente al socket
        como argumento.
        :param recibido: diccionario de la forma: {"status": tipo, "data":
        :param client_socket: socket correspondiente al cliente que envió
        '''

        if received['status'] == 'sign up':
            self.signup_client(client_socket, *received['data'])
        elif received['status'] == 'log in':
            self.login_client(client_socket, *received['data'])
        elif received['status'] == 'join waiting room':
            self.join_waiting_room(client_socket)
        elif received['status'] == 'waiting room':
            if received['command'] == 'new msg':
                self.new_msg(self.waiting_room, received['data'])
            elif received['command'] == 'start countdown':
                # definir la waiting room
                self.start_countdown(self.waiting_room)
            elif received['command'] == 'exit':
                self.exit_player(self.waiting_room, client_socket)
        elif received['status'] == 'game':
            if received['command'] == 'pause':
                self.pause_game(self.clients_game[client_socket])
            elif received['command'] == 'change direction':
                self.change_direction(self.clients_game[client_socket],
                                      received['data'], client_socket)
            elif received['command'] == 'start':
                self.start_game(self.clients_game[client_socket])

    def signup_client(self, client_socket, username, password1, password2):
        if self.server_users.get(username) is not None:
            msg = 'username'
        elif password1 != password2 or password1 == '':
            msg = 'password'
        else:
            sal, p_hash = self.encrypt_password(password1)
            self.server_users[username] = (sal, p_hash)
            msg = 'signed up'
            self.dump_server_users()
        response = {'status': self.clients[client_socket]['status'],
                    'command': 'sign up', 'data': msg}
        self.send(response, client_socket)

    def login_client(self, client_socket, username, password):
        user_info = self.server_users.get(username)
        if user_info is None:
            msg = 'username'
        elif username in self.users:
            msg = 'active'
        else:
            sal, db_hash = user_info
            sal, p_hash = self.encrypt_password(password, sal=sal)
            if not p_hash == db_hash:
                msg = 'password'
            else:
                msg = 'logged in'
                self.clients[client_socket]['status'] = msg
                self.clients[client_socket]['username'] = username
                self.users.add(username)
        response = {'status': self.clients[client_socket]['status'],
                    'command': 'log in', 'data': msg}
        self.send(response, client_socket)

    def load_server_users(self):
        with open('db_users.bin', 'rb') as file:
            self.server_users = pickle.load(file)

    def dump_server_users(self):
        with open('db_users.bin', 'bw') as file:
            pickle.dump(self.server_users, file)

    def encrypt_password(self, password, sal=None):
        if sal is None:
            sal = urandom(8)
        p = password.encode('UTF-8', errors='xmlcharrefreplace')
        m = sha256()
        m.update(sal + p)
        return sal, m.digest()

    def new_waiting_room(self):
        colors = ['red', 'blue', 'yellow', 'green', 'pink', 'light blue',
                 'orange', 'purple']
        colors = {color: None for color in colors}

        wr_data = {'players': {}, 'usernames': {}, 'powers': None,
                   'score': None, 'countdown': None, 'colors': colors,
                   'players number': {}}

        # crear un thread


    def join_new_waiting_room(self, client_socket):
        usernames = {1: self.clients[client_socket]['username']}
        players = {1: client_socket}
        colors[choice(list(colors.keys()))] = 1

    def join_waiting_room(self, client_socket):
        username = self.clients[client_socket]['username']
        r = self.waiting_room.add_player(client_socket, username)
        if not r:
            # return un diccionario sin la opción de ingresar
            d = {'status': 'rejected'}
            self.send(d, client_socket)
            return
        number, data = r
        self.clients[client_socket]['n'] = number
        self.clients[client_socket]['status'] = 'waiting room'
        d = {'status': 'waiting room', 'command': 'open', 'data': data,
             'n': number}
        self.send(d, client_socket)
        # depende de que wr es
        self.update_players_game(self.waiting_room)

    def send_to_all_players(self, players_sockets, data):
        for socket in players_sockets:
            self.send(data, socket)

    def update_players_waiting_room(self, players_sockets, command, data):
        d = {'status': 'waiting room', 'command': command, 'data': data}
        self.send_to_all_players(players_sockets, d)




    def waiting_room_thread(self, wr_data):
        pass

    def new_msg(self, waiting_room, msg):
        players_sockets, msg = waiting_room.new_msg(msg)
        self.update_players_waiting_room(players_sockets, 'new msg', msg)

    def update_players_game(self, waiting_room):
        players_sockets = waiting_room.players_sockets
        d = waiting_room.usernames_colors
        self.update_players_waiting_room(players_sockets, 'update players', d)

    def exit_player(self, waiting_room, client_socket):
        r = waiting_room.exit_player(client_socket)
        if r == 'countdown':
            return
        self.send({'status': 'exit'}, client_socket)
        self.users.remove(self.clients[client_socket]['username'])
        self.clients[client_socket] = {'status': 'not logged in', 'n': None,
                                       'username': None, 'game': None,
                                       'chief': None, 'score': None,
                                       'color': None, 'waiting room info': None}
        if r is not None:
            socket, n, data = r
            self.send({'status': 'waiting room', 'command': 'change chief',
                       'data': data, 'n': n}, socket)
        self.update_players_game(waiting_room)

    def start_countdown(self, waiting_room):
        if len(waiting_room.arrival) < 2:
            return
        players_sockets, colors, usernames, score = waiting_room.info_game()
        d = {'status': 'waiting room', 'command': 'start'}
        self.send_to_all_players(players_sockets.keys(), d)

        self.create_game(players_sockets, colors, usernames, score)

    ############## funciones del juego

    def create_game(self, players_sockets, colors, usernames, score):
        ''' los numeros de cada jugador están en p_sockets values'''
        game = Game(self, players_sockets, score)
        self.games[1] = game
        d = {socket: game for socket in players_sockets.keys()}
        self.clients_game.update(d)
        positions = game.set_positions()

        self.create_game_window(players_sockets, colors, positions, usernames,
                                score)


    def create_game_window(self, players_sockets, colors, positions,
                           usernames, score):
        score_text = {i: f'{username}:   0  |   {score} '
                      for i, username in usernames.items()}
        n = len(players_sockets)
        data = {'colors': colors, 'positions': positions, 'n': n,
                'scoretext': score_text}
        d = {'status': 'game', 'command': 'create', 'data': data}
        self.send_to_all_players(players_sockets, d)


    def game_thread(self,game, players_sockets):
        ''' funcion que recibe el socket y numero de cada jugador y crea
        el thread del juego.
        players_sockets: dict {socket: number}
        '''
        pass


    def start_game(self, game):
        with self.global_lock:
            if not game.started:
                game.started = True
                game.start()


    def change_direction(self, game, direction, player_socket):
        game.change_direction(direction, player_socket)

    def pause_game(self, game):
        game.pause_game()

    def update_positions(self, players_sockets, new_positions):
        self.send_to_all_players(players_sockets, {'status': 'game',
                          'command': 'update positions', 'data': new_positions})


if __name__ == "__main__":
    server = Server()

    while True:
        pass
