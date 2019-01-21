import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal, Qt

from key_setter_frontend import KeySetterWindow

class MainWindow(QWidget):

    def __init__(self, client):
        super().__init__()
        self.client = client # para mandar las señales
        self.init_GUI()

    def init_GUI(self):
        self.setGeometry(300, 200, 350, 300)
        self.login_button = QPushButton('Log In', self)
        self.signup_button = QPushButton('Sign Up', self)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.signup_button)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.login_button.clicked.connect(self.open_login_window)
        self.signup_button.clicked.connect(self.open_sign_up_window)

        self.signup_window = SignUpWindow(self.client, self)
        self.login_window = LogInWindow(self.client, self)

    def open_login_window(self):
        self.hide()
        self.login_window.show()

    def open_sign_up_window(self):
        self.hide()
        self.signup_window.show()

    def hide_login_window(self):
        self.login_window.hide()


class LogInWindow(QWidget):

    login_request_signal = pyqtSignal(str, str)

    def __init__(self, client, main_window):
        super().__init__()
        self.client = client
        self.main_window = main_window
        self.GUI()

    def GUI(self):
        self.setGeometry(300, 200, 350, 300)

        self.back_button = QPushButton('&Back', self)
        self.back_button.clicked.connect(self.return_main_window)

        self.msg_label = QLabel('', self)

        self.user_label = QLabel('Username')
        self.user_edit = QLineEdit('', self)
        self.password_label = QLabel('Password', self)
        self.password_edit = QLineEdit('', self)

        self.login_button = QPushButton('&Log In', self)
        self.login_button.clicked.connect(self.check_login)

        self.login_request_signal.connect(self.client.login_request)

        hbox = QHBoxLayout()
        hbox.addWidget(self.back_button)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch(.5)
        vbox.addWidget(self.user_label)
        vbox.addWidget(self.user_edit)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_edit)
        vbox.addStretch(.5)
        vbox.addWidget(self.msg_label)
        vbox.addStretch(.5)
        vbox.addWidget(self.login_button)
        self.setLayout(vbox)

    def check_login(self):
        user = self.user_edit.text()
        password = self.password_edit.text()
        self.login_request_signal.emit(user, password)

    def return_main_window(self):
        self.hide()
        self.main_window.show()

    def open_game(self, state):
        if state == 'logged in':
            return
        elif state == 'username':
            self.msg_label.setText('This username does not exists')
        elif state == 'password':
            self.msg_label.setText('Wrong password')
        elif state == 'active':
            self.msg_label.setText('You have already logged in')
        self.msg_label.resize(self.msg_label.sizeHint())


class SignUpWindow(QWidget):

    signup_request_signal = pyqtSignal(str, str, str)

    def __init__(self, client, main_window):
        super().__init__()
        self.client = client
        self.main_window = main_window
        self.init_GUI()

    def init_GUI(self):
        self.setGeometry(300, 200, 350, 300)

        self.back_button = QPushButton('&Back', self)
        self.back_button.clicked.connect(self.return_main_window)

        self.msg_label = QLabel('', self)

        self.user_label = QLabel('Username', self)
        self.user_edit = QLineEdit('', self)

        self.password_1_label = QLabel('Password', self)
        self.password_1_edit = QLineEdit('', self)

        self.password_2_label = QLabel('Confirm password', self)
        self.password_2_edit = QLineEdit('', self)

        self.register_button = QPushButton('&Sign Up', self)
        self.register_button.move(100, 250)
        self.register_button.clicked.connect(self.check_register)

        self.signup_request_signal.connect(self.client.signup_request)


        hbox =QHBoxLayout()
        hbox.addWidget(self.back_button)
        hbox.addStretch(1.5)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch(2)
        vbox.addWidget(self.user_label)
        vbox.addWidget(self.user_edit)
        vbox.addStretch(1)
        vbox.addWidget(self.password_1_label)
        vbox.addWidget(self.password_1_edit)
        vbox.addWidget(self.password_2_label)
        vbox.addWidget(self.password_2_edit)
        vbox.addStretch(.5)
        vbox.addWidget(self.msg_label)
        vbox.addStretch(.5)
        vbox.addWidget(self.register_button)
        self.setLayout(vbox)

    def return_main_window(self):
        self.hide()
        self.main_window.show()

    def check_register(self):
        user = self.user_edit.text()
        password1 = self.password_1_edit.text()
        password2 = self.password_2_edit.text()
        self.signup_request_signal.emit(user, password1, password2)

    def open_game(self, state):
        if state == 'signed up':
            self.msg_label.setText('Successful Sign Up')
        elif state == 'username':
            self.msg_label.setText('This user already exists')
        elif state == 'password':
            self.msg_label.setText('Wrong password')
        self.msg_label.resize(self.msg_label.sizeHint())

