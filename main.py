import sys
from io import BytesIO

import requests
import pygame
from distance import lonlat_distance


def draw_text(x, y, text, color=(255, 255, 255), size=30):
    font = pygame.font.SysFont("arial", size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "...",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

# аптека
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "..."
address_ll = ",".join([toponym_longitude, toponym_lattitude])
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
json_response = response.json()
organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])

# maps
p = ",".join([toponym_longitude, toponym_lattitude])
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": p,
    "l": "sat",
    "size": "650,450",
    "pt": f"{p},flag~{org_point},pma"
}
response = requests.get(map_api_server, params=map_params)
distance = lonlat_distance(tuple(map(float, p.split(","))),
                           tuple(map(float, org_point.split(","))))
print(distance)

pygame.init()
screen = pygame.display.set_mode((1150, 450))
image = pygame.image.load(BytesIO(response.content))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(image, (0, 0))
    draw_text(660, 10, "Аптека")
    draw_text(660, 50, org_name, size=20)
    draw_text(660, 80, org_address, size=20)
    draw_text(660, 110, org_time, size=20)
    draw_text(660, 140, "Растояние: " + f"{distance:.{0}f} м.", size=20)
    pygame.display.flip()
pygame.quit()
