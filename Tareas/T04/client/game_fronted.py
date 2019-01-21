
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QLineEdit, QHBoxLayout, QVBoxLayout,
                             QGraphicsScene, QGraphicsView, QMainWindow)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QPoint


# https://www.youtube.com/watch?v=2fv31ojiV5g&list=PL1FgJUcJJ03uwFW8
# ys2ov2dffKs3ieGYk&index=46

class GameWindow(QWidget):

    colors = {'magenta': Qt.magenta, 'red': Qt.red, 'yellow': Qt.yellow,
              'green': Qt.green, 'cyan': Qt.cyan, 'white': Qt.white}

    start_game_signal = pyqtSignal()
    change_direction_signal = pyqtSignal(str)
    pause_game_signal = pyqtSignal()

    def __init__(self, client, left_key, right_key, data):
        super().__init__()
        self.client = client
        self.left_key = left_key
        self.right_key = right_key
        self.initial_positions = {int(i): value
                                  for i, value in data['positions'].items()}
        self.score_text = data['scoretext']
        self.n_players = data['n']
        self.colornames = data['colors']
        self.colors = {i: GameWindow.colors[colorname]
                       for i, colorname in self.colornames.items()}

        self.init_GUI()
        #self.start_game_signal.connect(self.backend.start_game)
        self.change_direction_signal.connect(self.client.change_direction)
        self.pause_button.clicked.connect(self.pause_game)
        self.pause_game_signal.connect(self.client.pause_game_request)

    def init_GUI(self):
        self.setGeometry(100, 100, 768, 522)

        self.set_image()
        self.set_last_points()
        self.set_initial_points()

        self.score_label = QLabel('Score')
        self.score_label.setStyleSheet('color: white')
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.score_label)

        self.players_score_label = {}
        for i in range(1, int(self.n_players) + 1):
            text = self.score_text.get(str(i)) or self.score_text.get(i)
            label = QLabel(text, self)
            label.setStyleSheet(f'color: {self.colornames[str(i)]}')
            label.move(550, 200)
            self.players_score_label[i] = label
            vbox.addWidget(label)

        vbox.addStretch(1)

        self.pause_button = QPushButton('Pause', self)
        vbox.addWidget(self.pause_button)

        self.exit_button = QPushButton('Exit', self)
        vbox.addWidget(self.exit_button)

        self.new_game_button = QPushButton('New Game', self)
        vbox.addWidget(self.new_game_button)
        vbox.addStretch(1)

        hbox = QHBoxLayout(self)
        useles_label = QLabel('    '*13, self)
        hbox.addStretch(1)
        hbox.addWidget(useles_label)
        hbox.addLayout(vbox)


    def start(self):
        self.start_game_signal.emit()

    def set_image(self):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.black)
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
        painter.drawRect(28, 28, 452, 452)

    def set_last_points(self):
        self.last_points = {}
        for i in range(1, self.n_players + 1):
            x, y = self.initial_positions[i]
            self.last_points[i] = QPoint(x + 30, y + 30)

    def set_initial_points(self):
        for i in range(1, self.n_players + 1):
            color = self.colors[str(i)]
            painter = QPainter(self.image)
            painter.setPen(QPen(color, 3, Qt.SolidLine, Qt.RoundCap,
                                Qt.RoundJoin))
            painter.drawPoint(self.last_points[i])
            self.update()

    def update_positions(self, new_positions):
        painter = QPainter(self.image)
        for i in range(1, self.n_players + 1):
            color = self.colors[str(i)]
            painter.setPen(QPen(color, 3, Qt.SolidLine, Qt.RoundCap,
                                Qt.RoundJoin))
            x, y = new_positions[str(i)]
            new_point = QPoint(x + 30, y + 30)
            painter.drawLine(self.last_points[i], new_point)
            self.last_points[i] = new_point
            self.update()

    def paintEvent(self, e):
        algo = QPainter(self)
        algo.drawImage(self.rect(), self.image, self.image.rect())

    def keyPressEvent(self, e):
        if e.key() == self.left_key:
            self.change_direction_signal.emit('L')
        elif e.key() == self.right_key:
            self.change_direction_signal.emit('R')
        elif e.key() == Qt.Key_Space:
            self.pause_game_signal.emit()

    def pause_game(self):
        self.pause_game_signal.emit()


