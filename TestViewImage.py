import requests
import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

def geocode(address):
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    # Готовим запрос.
    geocoder_request = f'{server_address}apikey={api_key}&geocode={address}&format=json'

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    if not response:
        raise RuntimeError("Ошибка отправки запроса")
    json_response = response.json()
    if not json_response:
        raise RuntimeError("Пустой json")

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа, он находится по следующему пути:
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return toponym


def get_ll_span(toponym_to_find):
    toponym = geocode(toponym_to_find)
    if not toponym:
        return None, None
    toponym_coords = toponym["Point"]["pos"]
    top_longitube, top_lattitube = toponym_coords.split(" ")
    left, bottom = toponym["boundedBy"]["Envelope"]["lowerCorner"].split(" ")
    right, top = toponym["boundedBy"]["Envelope"]["upperCorner"].split(" ")
    dx = abs(float(left) - float(right))
    dy = abs(float(top) - float(bottom))
    span = f"{dx},{dy}"
    return top_longitube, top_lattitube, span


def get_coords_address(address):
    top = geocode(address)
    coords = top["Point"]["pos"].split(" ")
    top_longitube = float(coords[0])
    top_lattitube = float(coords[1])
    return top_longitube, top_lattitube


def get_components_address(address):
    top = geocode(address)
    return top["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]


toponym_to_find = "Литл-Сент-Джеймс"

toponym = geocode(toponym_to_find)
toponym_coodrinates = get_coords_address(toponym_to_find)
toponym_longitude, toponym_lattitude, span = get_ll_span(toponym_to_find)

delta = "0.005"
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
theme = "dark"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([str(toponym_longitude), str(toponym_lattitude)]),
    "spn": ",".join([delta, delta]),
    "apikey": apikey,
    "theme": theme,

}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()