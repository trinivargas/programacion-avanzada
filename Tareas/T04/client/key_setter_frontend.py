
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QLineEdit, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, pyqtSignal, Qt


class KeySetterWindow(QWidget):

    check_keys_signal = pyqtSignal(int, int, str, str)

    def __init__(self, client):
        super().__init__()
        self.direction = 'left'
        self.client = client
        self.init_GUI()
        self.right_key = None
        self.right_key_name = None
        self.left_key = None
        self.left_key_name = None

    def init_GUI(self):
        self.setGeometry(300, 200, 350, 300)
        self.msg1_label = QLabel('Choose the keys for movement', self)
        self.msg2_label = QLabel(f'Press a key to choose {self.direction} '
                                 f'movement')
        self.right_button = QPushButton('Right movement Key', self)
        self.right_button.clicked.connect(self.change_to_right_direction)
        self.right_key_label = QLabel('', self)
        self.left_button = QPushButton('Left movement Key', self)
        self.left_button.clicked.connect(self.change_to_left_direction)
        self.left_key_label = QLabel('', self)
        self.msg3_label = QLabel('', self)
        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.check_keys)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.msg1_label)
        vbox.addWidget(self.msg2_label)
        vbox.addStretch(.5)

        hbox = QHBoxLayout()
        hbox.addWidget(self.left_button)
        hbox.addWidget(self.right_button)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.left_key_label)
        hbox.addWidget(self.right_key_label)
        vbox.addLayout(hbox)
        vbox.addStretch(.4)
        vbox.addWidget(self.msg3_label)
        vbox.addStretch(.7)
        vbox.addWidget(self.next_button)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.check_keys_signal.connect(self.client.check_keys)


    def keyPressEvent(self, e):
        key_name = e.text().upper()
        if key_name == '':
            direction_keys = {16777235: 'Up', 16777236: 'Right',
                              16777234: 'Left', 16777237: 'Down'}
            key_name = direction_keys.get(e.key())
        elif key_name == ' ':
            key_name = 'Space'
        if self.direction == 'right':
            self.right_key = e.key()
            self.right_key_name = key_name
            self.right_key_label.setText(f'Chosen key: {key_name}')
            self.right_key_label.resize(self.right_key_label.sizeHint())
        elif self.direction == 'left':
            self.left_key = e.key()
            self.left_key_name = key_name
            self.left_key_label.setText(f'Chosen key: {key_name}')
            self.left_key_label.resize(self.left_key_label.sizeHint())

    def change_to_right_direction(self):
        self.direction = 'right'
        self.msg2_label.setText(f'Press a key to choose right movement')
        self.msg2_label.resize(self.msg2_label.sizeHint())

    def change_to_left_direction(self):
        self.direction = 'left'
        self.msg2_label.setText(f'Press a key to choose left movement')
        self.msg2_label.resize(self.msg2_label.sizeHint())

    def check_keys(self):
        self.check_keys_signal.emit(self.left_key, self.right_key,
                                    self.left_key_name, self.right_key_name)

    def open_waiting_room(self, state):
        if state == 'ok':
            self.msg3_label.setText('Ready')
        elif state == 'invalid':
            self.msg3_label.setText('One or more keys are invalid')
        elif state == 'same':
            self.msg3_label.setText('Left and right movent can not have the '
                                    'same key')
        self.msg3_label.resize(self.msg3_label.sizeHint())


