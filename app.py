import sys
import requests


from PyQt6.QtWidgets import QApplication
from PyQt6 import QtCore, QtWidgets

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


API_KEY = ""


class MapApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('MainWindow.ui', self)
        self.showMaximized()

        self.is_light_mode = True

        self.modes = [1, 2, 3]
        self.curr_mode_index = 0

        self.center_x = 0
        self.center_y = 0
        self.move_step = 0.0001
        self.min_cords = -180
        self.max_cords = 180

        self.scale = 1
        self.scale_step = 0.1
        self.min_scale = 0.1
        self.max_scale = 3

        self.search_button.clicked.connect(self.search_cords)
        self.search_address_button.clicked.connect(self.search_address)
        self.theme_button.clicked.connect(self.change_theme)
        self.mode_button.clicked.connect(self.change_mode)
        self.hui_button.clicked.connect(self.do_something)

    def update(self):
        print(self.is_light_mode)
        print(self.curr_mode_index, self.modes[self.curr_mode_index])
        print(self.center_x, self.center_y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            ...

        if event.key() == Qt.Key.Key_PageDown:
            ...

        if event.key() == Qt.Key.Key_Up:
            ...

        if event.key() == Qt.Key.Key_Down:
            ...

        if event.key() == Qt.Key.Key_Right:
            ...

        if event.key() == Qt.Key.Key_Left:
            ...

    def search_cords(self):
        x_text = self.longitube_edit.text()
        y_text = (self.lattitube_edit.text())

        if x_text:
            try:
                self.center_x = float(x_text)
            except ValueError:
                print("Координаты имеют формат float")

        if y_text:
            try:
                self.center_x = float(y_text)
            except ValueError:
                print("Координаты имеют формат float")

        self.update()

    def search_address(self):
        ...

    def change_theme(self):
        self.is_light_mode = not self.is_light_mode
        self.update()

    def change_mode(self):
        self.curr_mode_index += 1
        if self.curr_mode_index >= len(self.modes):
            self.curr_mode_index = 0
        self.update()

    def do_something(self):
        ...


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApplication()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
