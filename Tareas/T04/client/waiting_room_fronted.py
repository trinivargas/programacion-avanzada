import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QLineEdit, QHBoxLayout, QVBoxLayout, QCheckBox,
                             QScrollArea)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QObject, pyqtSignal, Qt


class ChiefWaitingRoomWindow(QWidget):

    send_msg_signal = pyqtSignal(str)
    change_color_signal = pyqtSignal(str)
    update_info_signal = pyqtSignal(dict)
    start_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self, client, data, n):
        super().__init__()
        self.client = client
        self.usernames = data['usernames']
        self.n = n
        self.username = self.usernames[str(n)]
        self.chief = data['chief']
        self.chat_msgs = data['new msgs']
        self.colors = data['colors']
        self.score = data['score']
        self.speed = data['speed']
        self.powers = data['powers']
        self.init_GUI()

        # conexion de botones
        self.start_button.clicked.connect(self.start_game)
        self.send_button.clicked.connect(self.send_msg)
        self.exit_button.clicked.connect(self.exit)

        # conexion de señales
        self.exit_signal.connect(self.client.exit_waiting_room_request)
        self.send_msg_signal.connect(self.client.send_msg)
        self.change_color_signal.connect(self.client.change_color_request)
        self.update_info_signal.connect(self.client.update_waiting_room_info)
        self.start_signal.connect(self.client.start_request)
        self.update_players(data['usernames colors'])

    def init_GUI(self):
        self.powers_label = QLabel('Powers')
        self.power_1_check_box = QCheckBox('Usain Nebolt', self)
        self.power_2_check_box = QCheckBox('Fernando Limpiessa', self)
        self.power_3_check_box = QCheckBox('Jaime Sinrastro', self)
        self.power_4_check_box = QCheckBox('Fernando Cervessa', self)
        self.power_5_check_box = QCheckBox('Felipe del Trio', self)
        self.power_6_check_box = QCheckBox('Nebcoins', self)

        # powers layout
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.powers_label)
        vbox1.addWidget(self.power_1_check_box)
        vbox1.addWidget(self.power_2_check_box)
        vbox1.addWidget(self.power_3_check_box)
        vbox1.addWidget(self.power_4_check_box)
        vbox1.addWidget(self.power_5_check_box)
        vbox1.addWidget(self.power_6_check_box)

        self.players_label = QLabel('Players', self)
        self.player_1_label = QLabel(f'Chief:', self)
        self.player_2_label = QLabel('Player 2: Waiting', self)
        self.player_3_label = QLabel('Player 3: Waiting', self)
        self.player_4_label = QLabel('Player 4: Waiting', self)
        self.players_labels = {1: self.player_1_label, 2: self.player_2_label,
                               3: self.player_3_label, 4: self.player_4_label}

        self.change_color_button = QPushButton('Change Color', self)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.players_label)
        vbox2.addWidget(self.player_1_label)
        vbox2.addWidget(self.player_2_label)
        vbox2.addWidget(self.player_3_label)
        vbox2.addWidget(self.player_4_label)
        vbox2.addWidget(self.change_color_button)

        hbox1 = QHBoxLayout() # contiene los poderes y jugadores
        hbox1.addStretch(.5)
        hbox1.addLayout(vbox1)
        hbox1.addStretch(2.3)
        hbox1.addLayout(vbox2)
        hbox1.addStretch(1)

        self.chat_scroll = QScrollArea(self)
        self.chat_scroll.setFixedSize(250, 140)
        self.chat_scroll.setWidgetResizable(True)
        self.chat_msgs_label = QLabel('', self)
        self.chat_scroll.setWidget(self.chat_msgs_label)

        self.chat_edit = QLineEdit('', self)
        self.send_button = QPushButton('Send')

        hbox = QHBoxLayout()
        hbox.addWidget(self.chat_edit)
        hbox.addWidget(self.send_button)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.chat_scroll)
        vbox3.addLayout(hbox)

        self.score_label = QLabel('Score: ', self)
        self.score_edit = QLineEdit(str(self.score), self)

        self.speed_label = QLabel('Speed', self)
        self.speed_edit = QLineEdit(str(self.speed), self)

        self.start_button = QPushButton('Start', self)
        self.exit_button = QPushButton('Exit', self)
        self.countdown_label = QLabel('   10', self)
        font = QFont('', 40, QFont.Bold)
        self.countdown_label.setFont(font)
        self.msg = QLabel('', self)

        vbox4 = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addWidget(self.score_label)
        hbox.addWidget(self.score_edit)
        vbox4.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.speed_label)
        hbox.addWidget(self.speed_edit)
        vbox4.addLayout(hbox)

        vbox4.addWidget(self.msg)
        vbox4.addWidget(self.countdown_label)
        vbox4.addWidget(self.start_button)
        vbox4.addWidget(self.exit_button)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addLayout(vbox3)
        hbox2.addStretch(1)
        hbox2.addLayout(vbox4)
        hbox2.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(2)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def add_player(self, number, user_name, color):
        if number == 1:
            self.player_1_label.setText(f'Chief: {user_name}')
            self.player_1_label.resize(self.player_1_label.sizeHint())
        elif number == 2:
            self.player_2_label.setText(f'Player 2: {user_name}')
            self.player_2_label.resize(self.player_2_label.sizeHint())
        elif number == 3:
            self.player_3_label.setText(f'Player 3: {user_name}')
            self.player_3_label.resize(self.player_3_label.sizeHint())
        elif number == 4:
            self.player_4_label.setText(f'Player 4: {user_name}')
            self.player_4_label.resize(self.player_4_label.sizeHint())

    def start_game(self):
        self.start_signal.emit()

    def send_msg(self):
        msg = f'{self.username}: {self.chat_edit.text()}\n'
        self.chat_edit.setText("")
        self.send_msg_signal.emit(msg)

    def update_chat(self, msg):
        self.chat_msgs += msg
        self.chat_msgs_label.setText(self.chat_msgs)

    def exit(self):
        self.exit_signal.emit()

    def update_count_down(self, n):
        self.countdown_label.setText(f'    {n}')
        self.countdown_label.resize(self.countdown_label.sizeHint())

    def update_players(self, players_color):
        ''' recibe un diccionario del tipo {1: (username, color)}'''
        for i in range(1, 5):
            label = self.players_labels[i]
            user_color = players_color.get(str(i))
            if user_color is None:
                label.setText(f'Player {i}: Waiting')
                label.setStyleSheet('color: black')
            else:
                username, color = user_color
                if i == 1:
                    label.setText(f'Player {i}: {username} (chief)')
                else:
                    label.setText(f'Player {i}: {username}')
                label.setStyleSheet(f'color: {color}')


class WaitingRoomWindow(QWidget):
    colors = {'red': Qt.red, 'yellow': Qt.yellow, 'blue': Qt.blue,
              'green': Qt.green}

    send_msg_signal = pyqtSignal(str)
    change_color_signal = pyqtSignal(str)
    exit_signal = pyqtSignal()

    def __init__(self, client, data, n):
        super().__init__()
        self.client = client
        self.usernames = data['usernames']
        self.n = n
        self.username = self.usernames[str(n)]
        self.chief = data['chief']
        self.chat_msgs = data['new msgs']
        self.colors = data['colors']
        self.score = data['score']
        self.powers = data['powers']
        self.init_GUI()
        self.update_players(data['usernames colors'])

        # conexion de botones
        self.send_button.clicked.connect(self.send_msg)
        self.exit_button.clicked.connect(self.exit)

        # conexion de señales
        self.exit_signal.connect(self.client.exit_waiting_room_request)
        self.send_msg_signal.connect(self.client.send_msg)
        self.change_color_signal.connect(self.client.change_color_request)

    def init_GUI(self):
        self.powers_label = QLabel('Powers')
        self.powers_list = QLabel('\n\n\n\n\n\n', self)

        # powers layout
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.powers_label)
        vbox1.addWidget(self.powers_list)

        self.players_label = QLabel('Players', self)
        self.player_1_label = QLabel(f'Chief: {self.usernames["1"]}', self)
        self.player_2_label = QLabel('Player 2: Waiting', self)
        self.player_3_label = QLabel('Player 3: Waiting', self)
        self.player_4_label = QLabel('Player 4: Waiting', self)
        self.players_labels = {1: self.player_1_label, 2: self.player_2_label,
                              3: self.player_3_label, 4: self.player_4_label}
        # change color puede ser QComboBox
        self.change_color_button = QPushButton('Change Color', self)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.players_label)
        vbox2.addWidget(self.player_1_label)
        vbox2.addWidget(self.player_2_label)
        vbox2.addWidget(self.player_3_label)
        vbox2.addWidget(self.player_4_label)
        vbox2.addWidget(self.change_color_button)

        hbox1 = QHBoxLayout() # contiene los poderes y jugadores
        hbox1.addStretch(.5)
        hbox1.addLayout(vbox1)
        hbox1.addStretch(2.3)
        hbox1.addLayout(vbox2)
        hbox1.addStretch(1)

        self.chat_scroll = QScrollArea(self)
        self.chat_scroll.setFixedSize(250, 100)
        self.chat_scroll.setWidgetResizable(True)
        self.chat_msgs_label = QLabel('', self)
        self.chat_scroll.setWidget(self.chat_msgs_label)

        self.chat_edit = QLineEdit('', self)
        self.send_button = QPushButton('Send')

        hbox = QHBoxLayout()
        hbox.addWidget(self.chat_edit)
        hbox.addWidget(self.send_button)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.chat_scroll)
        vbox3.addLayout(hbox)

        self.score_label = QLabel(f'Score: 150', self)
        self.exit_button = QPushButton('Exit', self)
        self.countdown_label = QLabel('   10', self)
        font = QFont('', 40, QFont.Bold)
        self.countdown_label.setFont(font)
        self.msg = QLabel('', self)

        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.score_label)
        vbox4.addWidget(self.msg)
        vbox4.addWidget(self.countdown_label)
        vbox4.addWidget(self.exit_button)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addLayout(vbox3)
        hbox2.addStretch(1)
        hbox2.addLayout(vbox4)
        hbox2.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(3)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def add_player(self, number, user_name, color):
        if number == 1:
            self.player_1_label.setText(f'Chief: {user_name}')
            self.player_1_label.resize(self.player_1_label.sizeHint())
        elif number == 2:
            self.player_2_label.setText(f'Player 2: {user_name}')
            self.player_2_label.resize(self.player_2_label.sizeHint())
        elif number == 3:
            self.player_3_label.setText(f'Player 3: {user_name}')
            self.player_3_label.resize(self.player_3_label.sizeHint())
        elif number == 4:
            self.player_4_label.setText(f'Player 4: {user_name}')
            self.player_4_label.resize(self.player_4_label.sizeHint())


    def send_msg(self):
        msg = f'{self.username}: {self.chat_edit.text()}\n'
        self.chat_edit.setText("")
        self.send_msg_signal.emit(msg)

    def update_chat(self, msg):
        self.chat_msgs += msg
        self.chat_msgs_label.setText(self.chat_msgs)

    def update_score(self, score):
        self.score_label.setText(f'Score: {score}')

    def update_powers(self, powers):
        self.powers_list = powers
        self.powers_label.setText(self.powers_list)

    def exit(self):
        self.exit_signal.emit()

    def update_count_down(self, n):
        self.countdown_label.setText(f'    {n}')
        self.countdown_label.resize(self.countdown_label.sizeHint())

    def update_players(self, players_color):
        ''' recibe un diccionario del tipo {1: (username, color)}'''
        for i in range(1, 5):
            label = self.players_labels[i]
            user_color = players_color.get(str(i))
            if user_color is None:
                label.setText(f'Player {i}: Waiting')
                label.setStyleSheet('color: black')
            else:
                username, color = user_color
                if i == 1:
                    label.setText(f'Player {i}: {username} (chief)')
                else:
                    label.setText(f'Player {i}: {username}')
                label.setStyleSheet(f'color: {color}')
            label.resize(label.sizeHint())

