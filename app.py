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

    def update(self):
        ...

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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MapApplication()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
