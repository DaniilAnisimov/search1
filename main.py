import sys
from io import BytesIO

import requests
import pygame
from spn import spn


toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "...",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = toponym["boundedBy"]["Envelope"]
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": spn(delta["lowerCorner"], delta["upperCorner"]),
    "l": "sat",
    "size": "650,450",
    "pt": f"{','.join([toponym_longitude, toponym_lattitude])},flag"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

pygame.init()
screen = pygame.display.set_mode((650, 450))
screen.blit(pygame.image.load(BytesIO(response.content)), (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()