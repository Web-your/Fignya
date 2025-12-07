import sys
import random
from PyQt6 import QtWidgets, uic, QtGui, QtCore


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.circles = []
        self.pushButton.clicked.connect(self.add_circle)

    def add_circle(self):
        diameter = random.randint(20, 120)
        x = random.randint(0, self.width() - diameter)
        y = random.randint(0, self.height() - diameter)

        self.circles.append((x, y, diameter))
        self.update()  # перерисовать окно

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for x, y, d in self.circles:
            painter.setBrush(QtGui.QBrush(QtGui.QColor("yellow")))
            painter.setPen(QtGui.QPen(QtGui.QColor("yellow")))
            painter.drawEllipse(x, y, d, d)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())