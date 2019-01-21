import sys
from PyQt5.QtWidgets import QApplication
import threading
import socket
import json
from PyQt5.QtCore import pyqtSignal, QObject
from time import sleep

from frontend import GameWindows
PORT = 8081
# código sacado de la ayudantia 13 2018-1

class Client(QObject):

    signup_signal = pyqtSignal(str)
    login_signal = pyqtSignal(str)
    open_keys_setter_window_signal = pyqtSignal()
    check_keys_signal = pyqtSignal(str)
    open_waiting_room_window_signal = pyqtSignal(dict, int)
    change_waiting_room_signal = pyqtSignal(dict, int)
    new_msg_signal = pyqtSignal(str)
    count_down_signal = pyqtSignal(int)
    update_players_signal = pyqtSignal(dict)
    exit_waiting_room_signal = pyqtSignal()
    create_game_window_signal = pyqtSignal(int, int, dict)
    open_game_signal = pyqtSignal()
    update_positions_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        print("Inicializando cliente...")

        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = PORT
        self.username = None

        try:
            self.socket_cliente.connect((self.host, self.port))
            print("Cliente conectado exitosamente al servidor...")

            self.connected = True
            self.status = None

            thread = threading.Thread(target=self.listen_thread, daemon=True)
            thread.start()
            print("Escuchando al servidor...")
            self.game_windows = GameWindows(self) # MainWindow(self)

            self.login_signal.connect(self.game_windows.login_window.open_game)
            self.signup_signal.connect(
                self.game_windows.signup_window.open_game)
            self.open_keys_setter_window_signal.connect(
                self.game_windows.open_keys_setter_window)
            self.open_waiting_room_window_signal.connect(
                self.game_windows.open_waiting_room_window)
            self.check_keys_signal.connect(
                self.game_windows.keys_setter_window.open_waiting_room)
            self.exit_waiting_room_signal.connect(
                self.game_windows.exit_waiting_room)
            self.create_game_window_signal.connect(
                self.game_windows.create_game)
            self.open_game_signal.connect(self.game_windows.start_playing)
            self.change_waiting_room_signal.connect(
                self.game_windows.change_to_waiting_room_window)
            self.countdown0 = threading.Event()
            self.game_created = threading.Event()

        except ConnectionRefusedError:
            print("Conexión terminada")
            self.socket_cliente.close()
            exit()

    def listen_thread(self):
        '''
        Este método es el usado en el thread y la idea es que reciba lo que
        envía el servidor. Implementa el protocolo de agregar los primeros
        4 bytes, que indican el largo del mensaje
        :return:
        '''

        while self.connected:
            response_bytes_length = self.socket_cliente.recv(4)
            response_length = int.from_bytes(response_bytes_length,
                                             byteorder="big")

            response = bytearray()
            while len(response) < response_length:
                response += self.socket_cliente.recv(256)

            response = response.decode()
            decoded = json.loads(response)
            self.handlecommand(decoded)

    def send(self, msg):
        '''
        Este método envía la información al servidor. Recibe un mensaje del tipo
        {"status": tipo del mensaje, "data": información}
        :param msg: diccionario con la información
        :return:
        '''

        # Le hacemos json.dumps y luego lo transformamos a bytes
        msg_json = json.dumps(msg)
        msg_bytes = msg_json.encode()

        # Luego tomamos el largo de los bytes y creamos 4 bytes de esto
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")

        # Finalmente, los enviamos al servidor
        self.socket_cliente.send(msg_length + msg_bytes)

    def handlecommand(self, received):
        if received['status'] == 'not logged in' or \
                received['status'] == 'logged in':
            if received['command'] == 'log in':
                self.login_response(received['data'])
            elif received['command'] == 'sign up':
                self.signup_response(received['data'])

        elif received['status'] == 'waiting room':
            if received['command'] == 'open':
                self.waiting_room_response(received)
            elif received['command'] == 'new msg':
                self.new_msg(received['data'])
            elif received['command'] == 'update players':
                self.update_players(received['data'])
            elif received['command'] == 'start':
                self.start_countdown()
            elif received['command'] == 'change chief':
                self.change_waiting_room(received)
                print('jujujuju')

        elif received['status'] == 'game':
            if received['command'] == 'update positions':
                self.update_positions(received['data'])
            elif received['command'] == 'create':
                self.create_game(received['data'])
                self.open_game()
            elif received['command'] == 'open game':
                self.open_game()
            elif received['command'] == 'start':
                pass
        elif received['status'] == 'exit':
            self.exit_waiting_room()

    ######## funciones de log in ############
    def login_request(self, username, password):
        ''' esta función la llama el frontend '''
        self.send({'status': 'log in', 'data': (username, password)})

    def login_response(self, response):
        print('response login')
        if response == 'logged in':
            self.open_keys_setter_window_signal.emit()

        else:
            self.login_signal.emit(response)

    def signup_request(self, username, password1, password2):
        self.send({'status': 'sign up', 'data': (username, password1,
                                                 password2)})

    def signup_response(self, response):
        self.signup_signal.emit(response)

    ############## funciones de set keys ################
    def check_keys(self, left_key, right_key, left_key_name, right_key_name):
        if not left_key_name or not right_key_name:
            self.check_keys_signal.emit('invalid')
        elif left_key == right_key:
            self.check_keys_signal.emit('same')
        else:
            self.check_keys_signal.emit('ok')
            self.left_key = left_key
            self.right_key = right_key
            self.waiting_room_request()

    ########### funciones de waiting room ###############
    def waiting_room_request(self):
        self.send({'status': 'join waiting room'})

    def waiting_room_response(self, received):
        if received['status'] == 'rejected':
            return
        self.open_waiting_room_window_signal.emit(received['data'],
                                                  received['n'])

    def connect_wr_signals(self):
        self.waiting_room = self.game_windows.waiting_room_window
        self.new_msg_signal.connect(self.waiting_room.update_chat)
        self.count_down_signal.connect(self.waiting_room.update_count_down)
        self.update_players_signal.connect(self.waiting_room.update_players)


    #def open_waiting_room(self, player_number):
     #   self.open_waiting_room_window_signal.emit(player_number)

    def update_waiting_room_info(self, data):
        pass

    def start_request(self):
        d = {'status': 'waiting room', 'command': 'start countdown'}
        self.send(d)

    def exit_waiting_room_request(self):
        d = {'status': 'waiting room', 'command': 'exit'}
        self.send(d)

    def exit_waiting_room(self):
        self.exit_waiting_room_signal.emit()

    def change_waiting_room(self, received):
        # retorna received['data'], received[n]
        self.change_waiting_room_signal.emit(received['data'], received['n'])
        print('yeiii')

    def send_msg(self, msg):
        d = {'status': 'waiting room', 'command': 'new msg', 'data': msg}
        self.send(d)

    def new_msg(self, msg):
        self.new_msg_signal.emit(msg)

    def change_color_request(self, color):
        pass

    def update_players(self, players_color):
        self.update_players_signal.emit(players_color)

    def start_countdown(self):
        count_down = threading.Thread(target=self.count_down)
        count_down.start()

    def count_down(self):
        for i in range(9, -1, -1):
            self.count_down_signal.emit(i)
            sleep(1)
        self.countdown0.set()

    ############# funciones para el juego

    def create_game(self, data):
        print('##### data', data)
        self.create_game_window_signal.emit(self.left_key, self.right_key,
                                            data)

    def connect_game_signals(self):
        self.game_window = self.game_windows.game_window
        self.update_positions_signal.connect(self.game_window.update_positions)
        self.game_created.set()

    def change_direction(self, d):
        self.send({'status': 'game', 'command': 'change direction', 'data': d})

    def open_game(self):
        self.countdown0.wait()
        self.game_created.wait()
        self.open_game_signal.emit()
        self.send({'status': 'game', 'command': 'start'})

    def update_positions(self, new_positions):
        ''' new_positions es un dict de la forma {i: x, y}'''
        self.update_positions_signal.emit(new_positions)

    def pause_game_request(self):
        self.send({'status': 'game', 'command': 'pause'})





if __name__ == "__main__":
    app = QApplication([])
    client = Client()
    sys.exit(app.exec_())


