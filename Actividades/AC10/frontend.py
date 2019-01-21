# Acá va lo relacionado con la GUI.

# EL codigo esta basado en la ayudantia !!!

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from backend import NameChecker, Pacman

from random import randint

class MainWindow(QWidget):

    check_name_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setGeometry(13, 8, 500, 400)
        self.init_GUI()

    def init_GUI(self):
        self.label0 = QLabel('Bienvenido a Pacman!', self)
        self.label0.move(10, 15)
        self.label1 = QLabel('Nombre:', self)
        self.label1.move(10, 45)
        self.label2 = QLabel('', self)
        self.label2.move(50, 100)

        self.edit1 = QLineEdit('', self)
        self.edit1.setGeometry(75, 45, 100, 20)
        self.boton1 = QPushButton('Inicio', self)
        self.boton1.move(5, 70)
        self.boton1.clicked.connect(self.check_name)

        self.spell_checker = NameChecker(self)
        self.check_name_signal.connect(self.spell_checker.check)

    def check_name(self):
        nombre_usuario = self.edit1.text()
        self.check_name_signal.emit(nombre_usuario)

    def open_window(self, state):
        """
        Función que dado un estado, cambia la ventana de inicio por la del juego.
        :param state: bool
        :return: none
        """
        if state:
            self.hide()
            self.maingame = MainGame()
            self.maingame.show()
        if not state:
            # solo cambia si cambias el tamaño de la ventana con el mouse
            self.label2.setText('No cumple las condiciones necesarias')
            self.label2.resize(self.label2.sizeHint())



class MainGame(QWidget):

    move_pacman_signal = pyqtSignal(str)
    #new_guindas_signal = pyqtSignal(bool)


    def __init__(self):
        super().__init__()
        self.setGeometry(13, 8, 560, 615) # no respeté lo del enuncado porque
        # no se alcanzaba a ver to do el mapa

        self._frame = 1

        # Se setea la imagen de fondo.
        se

        # Se instancia el personaje del backend y se conecta move_character_signal con la función
        # move de Character.
        self.backend_character = Pacman(self, 280, 305)
        self.move_pacman_signal.connect(self.backend_character.move)

        # Se crea el personaje en el frontend.
        self.front_pacman = QLabel(self)
        self.front_pacman.setPixmap(QPixmap('sprites/pacman_R_1.png'))
        self.front_pacman.move(280, 305)

        self.guindas = set()

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value > 3:
            self._frame = 1
        else:
            self._frame = value

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Right:
            self.frame += 1
            self.front_pacman.setPixmap(QPixmap(
                f'sprites/pacman_R_{self.frame}.png'))
            self.move_pacman_signal.emit('R')
        if e.key() == Qt.Key_Left:
            self.frame += 1
            self.front_pacman.setPixmap(QPixmap(
                f'sprites/pacman_L_{self.frame}.png'))
            self.move_pacman_signal.emit('L')
        if e.key() == Qt.Key_Down:
            self.frame += 1
            self.front_pacman.setPixmap(QPixmap(
                f'sprites/pacman_D_{self.frame}.png'))
            self.move_pacman_signal.emit('D')
        if e.key() == Qt.Key_Up:
            self.frame += 1
            self.front_pacman.setPixmap(QPixmap(
                f'sprites/pacman_U_{self.frame}.png'))
            self.move_pacman_signal.emit('U')
        if e.key() == Qt.Key_Space:
            self.nuevas_guindas()

    def update_position(self, event):
        self.front_pacman.move(event['x'], event['y'])

    def nuevas_guindas(self):
        g_x, g_y = randint(0, 540), randint(0, 590)
        guinda = QLabel(self)
        guinda.setPixmap(QPixmap('sprites/cherry.png'))
        guinda.move(g_x, g_y)
        guinda.show()
        self.guindas.add(guinda)


if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())