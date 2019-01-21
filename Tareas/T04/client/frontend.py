import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QLineEdit, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, pyqtSignal, Qt

from main_window_frontend import MainWindow, LogInWindow, SignUpWindow
from key_setter_frontend import KeySetterWindow
from waiting_room_fronted import ChiefWaitingRoomWindow, WaitingRoomWindow
from game_fronted import GameWindow


class GameWindows(QWidget):

    waiting_room_ready_signal = pyqtSignal()
    game_window_ready_signal = pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.main_window = MainWindow(self.client)
        self.login_window = self.main_window.login_window
        self.signup_window = self.main_window.signup_window
        self.keys_setter_window = KeySetterWindow(self.client)
        self.init_game()

        self.game_window_ready_signal.connect(self.client.connect_game_signals)
        self.waiting_room_ready_signal.connect(self.client.connect_wr_signals)

    def init_game(self):
        self.main_window.show()

    def open_keys_setter_window(self):
        self.login_window.hide()
        self.keys_setter_window.show()
        del self.main_window
        del self.login_window
        del self.signup_window

    def open_waiting_room_window(self, data, n):
        chief = bool(data['chief'] == n)
        if chief:
            self.waiting_room_window = ChiefWaitingRoomWindow(self.client,
                                                              data, n)
        else:
            self.waiting_room_window = WaitingRoomWindow(self.client, data, n)
        self.keys_setter_window.hide()
        self.waiting_room_window.show()

        self.waiting_room_ready_signal.emit()

    def exit_waiting_room(self):
        self.waiting_room_window.hide()
        self.main_window = MainWindow(self.client)
        self.login_window = self.main_window.login_window
        self.signup_window = self.main_window.signup_window
        self.keys_setter_window = KeySetterWindow(self.client)
        del self.waiting_room_window
        self.init_game()

    def create_game(self, left_key, right_key, data):
        self.game_window = GameWindow(self.client, left_key, right_key, data)
        self.game_window_ready_signal.emit()

    def start_playing(self):
        self.waiting_room_window.hide()
        self.game_window.show()
        del self.waiting_room_window

    def new_waiting_room_window(self, data, n):
        self.game_window.hide()
        self.open_waiting_room_window(data, n)

    def change_to_waiting_room_window(self, data, n):
        self.waiting_room_window.hide()
        wr = ChiefWaitingRoomWindow(self.client, data, n)
        wr.show()
        del self.waiting_room_window
        self.waiting_room_window = wr
        self.waiting_room_ready_signal.emit()


