# Acá va lo relacionado con el procesamiento de datos

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.Qt import QTest

class NameChecker(QObject):

    check_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.check_signal.connect(parent.open_window)

    def check(self, nombre):
        if not nombre.isalpha() or len(nombre) < 7:
            self.check_signal.emit(False)
            print('No funciona')
        else:
            self.check_signal.emit(True)
            print('Jugando')


class Pacman(QObject):

    update_position_signal = pyqtSignal(dict)

    def __init__(self,  parent, x, y):
        super().__init__()
        self.direction = 'R'
        self._x = x
        self._y = y
        self.update_position_signal.connect(parent.update_position)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if 0 < value < 540:
            self._x = value
            self.update_position_signal.emit({'x': self.x, 'y': self.y})

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if 0 < value < 590:
            self._y = value
            self.update_position_signal.emit({'x': self.x, 'y': self.y})

    def move(self, event):
        if event == 'R':
            self.x += 10
            self.direction = 'R'
        if event == 'L':
            self.x -= 10
            self.direction = 'L'
        if event == 'U':
            self.direction = 'U'
            self.y -= 10
        if event == 'D':
            self.direction = 'D'
            self.y += 10

