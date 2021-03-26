import sys

import pygame
import requests

from io import BytesIO

from spn import spn
import random


# Программа грузит картинки где то 5 - 15 секунд

def main():
    cities = ["Астрахань", "Москва", "Ташкент", "Санкт-Петербург",
              "Владивосток", "Кострома", "Анапа"]
    api_server = "http://static-maps.yandex.ru/1.x/"
    p = True
    photo = []
    for city in cities:
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "",
            "geocode": city,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]

        delta = toponym["boundedBy"]["Envelope"]
        lon, lat = toponym["Point"]["pos"].split()
        params = {
            "ll": ",".join([lon, lat]),
            "l": "sat",
            "size": "450,450",
            "spn": spn(delta["lowerCorner"], delta["upperCorner"]),
            "pt": ",".join([str(float(lon) + 0.0003), str(float(lat) + 0.0001)]) + ",flag"
        }
        response = requests.get(api_server, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        photo.append(pygame.image.load(BytesIO(response.content)))

    pygame.init()
    screen = pygame.display.set_mode((450, 450))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN or p:
                p = False
                i = random.randint(0, len(cities) - 1)
                screen.blit(photo[i], (0, 0))
                pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
