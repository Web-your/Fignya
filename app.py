import sys
import requests
from io import BytesIO

from PyQt6.QtWidgets import QApplication
from PyQt6 import QtCore, QtWidgets

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MapApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('MainWindow.ui', self)

        self.apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

        self.themes = ["dark", "light"]
        self.is_light_mode = True

        self.modes = ["map", "driving", "transit", "admin"]
        self.curr_mode_index = 0

        self.center_x = 37.6174994
        self.move_step_x = 1
        self.min_cords_x = -180
        self.max_cords_x = 180

        self.center_y = 55.7520233
        self.move_step_y = 0.00001
        self.min_cords_y = -70
        self.max_cords_y = 70

        self.zoom = 15
        self.zoom_step = 1
        self.min_zoom = 0
        self.max_zoom = 21

        self.map_params = {
            "apikey": self.apikey,
            "ll": ",".join([str(self.center_x), str(self.center_y)]),
            "z": self.zoom,
            "size": ",".join([
                str(650),
                str(450)
            ]),
            "theme": self.themes[int(self.is_light_mode)],
            "maptype": self.modes[self.curr_mode_index],
            "lang": "ru_RU"
        }

        img = get_map_img(self.map_params)
        pm_img = QPixmap()
        pm_img.loadFromData(img)
        self.label.setPixmap(pm_img)

        self.search_button.clicked.connect(self.search_cords)
        self.search_address_button.clicked.connect(self.search_address)
        self.theme_button.clicked.connect(self.change_theme)
        self.mode_button.clicked.connect(self.change_mode)
        self.hui_button.clicked.connect(self.do_something)

        self.on_update()

    def on_update(self):
        self.map_params = {
            "apikey": self.apikey,
            "ll": ",".join([str(self.center_x), str(self.center_y)]),
            "z": self.zoom,
            "size": ",".join([
                str(650),
                str(450)
            ]),
            "theme": self.themes[int(self.is_light_mode)],
            "maptype": self.modes[self.curr_mode_index],
            "lang": "ru_RU"
        }

        img = get_map_img(self.map_params)
        pm_img = QPixmap()
        pm_img.loadFromData(img)
        self.label.setPixmap(pm_img)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.zoom += self.zoom_step
            self.zoom = min(self.zoom, self.max_zoom)

        if event.key() == Qt.Key.Key_PageDown:
            self.zoom -= self.zoom_step
            self.zoom = max(self.zoom, self.min_zoom)

        if event.key() == Qt.Key.Key_Up:
            self.center_y += self.move_step_y * 2 ** (self.max_zoom - self.zoom)
            self.center_y = min(self.center_y, self.max_cords_y)

        if event.key() == Qt.Key.Key_Down:
            self.center_y -= self.move_step_y * 2 ** (self.max_zoom - self.zoom)
            self.center_y = max(self.center_y, self.min_cords_y)

        if event.key() == Qt.Key.Key_Right:
            self.center_x += self.move_step_x * 2 ** (self.max_zoom - self.zoom)
            self.center_x %= 360
            if self.center_x > 180:
                self.center_x = -(self.center_x - 180)


        if event.key() == Qt.Key.Key_Left:
            self.center_x -= self.move_step_x * 2 ** (self.max_zoom - self.zoom)
            self.center_y %= 180
            if self.center_y > 90:
                self.center_y = -(self.center_y - 90)

        self.on_update()

    def search_cords(self):
        x_text = self.longitube_edit.text()
        y_text = (self.lattitube_edit.text())

        if x_text:
            try:
                self.center_x = float(x_text)
                self.center_x %= 360
                if self.center_x > 180:
                    self.center_x = -(self.center_x - 180)
            except ValueError:
                print("Координаты имеют формат float")

        if y_text:
            try:
                self.center_y = float(y_text)
                self.center_y %= 180
                if self.center_y > 90:
                    self.center_y = -(self.center_y - 90)
            except ValueError:
                print("Координаты имеют формат float")

        self.on_update()

    def search_address(self):
        ...

    def change_theme(self):
        self.is_light_mode = not self.is_light_mode
        self.on_update()

    def change_mode(self):
        self.curr_mode_index += 1
        if self.curr_mode_index >= len(self.modes):
            self.curr_mode_index = 0
        self.on_update()

    def do_something(self):
        ...


def geocode(address):
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    geocoder_request = f'{server_address}apikey={api_key}&geocode={address}&format=json'
    response = requests.get(geocoder_request)

    if not response:
        raise RuntimeError("Ошибка отправки запроса")
    json_response = response.json()
    if not json_response:
        raise RuntimeError("Пустой json")

    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return toponym


def get_ll_span(toponym_to_find):
    toponym = geocode(toponym_to_find)
    if not toponym:
        return None, None
    toponym_cords = toponym["Point"]["pos"]
    top_longitude, top_latitude = toponym_cords.split(" ")
    left, bottom = toponym["boundedBy"]["Envelope"]["lowerCorner"].split(" ")
    right, top = toponym["boundedBy"]["Envelope"]["upperCorner"].split(" ")
    dx = abs(float(left) - float(right))
    dy = abs(float(top) - float(bottom))
    span = f"{dx},{dy}"
    return top_longitude, top_latitude, span


def get_cords_address(address):
    top = geocode(address)
    cords = top["Point"]["pos"].split(" ")
    top_longitude = float(cords[0])
    top_latitude = float(cords[1])
    return top_longitude, top_latitude


def get_components_address(address):
    top = geocode(address)
    return top["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]


def get_map_img(map_params):
    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    img_bytes = BytesIO(response.content)
    return img_bytes.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApplication()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
