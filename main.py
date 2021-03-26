import sys
from io import BytesIO

import requests
import pygame

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
pharmacies = []
for i in range(min(10, len(json_response["features"]))):
    organization = json_response["features"][i]
    org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    if "круглосуточно" in org_time or "24" in org_time:
        flag = "pm2gnm"
    elif org_time == "":
        flag = "pm2grm"
    else:
        flag = "pm2blm"
    pharmacies.append(f"{org_point},{flag}")

# maps
p = ",".join([toponym_longitude, toponym_lattitude])
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": p,
    "l": "sat",
    "size": "450,450",
    "pt": "~".join(pharmacies)
}
response = requests.get(map_api_server, params=map_params)

pygame.init()
screen = pygame.display.set_mode((450, 450))
image = pygame.image.load(BytesIO(response.content))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(image, (0, 0))
    pygame.display.flip()
pygame.quit()
