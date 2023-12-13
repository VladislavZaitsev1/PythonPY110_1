import json

import requests
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}

print('Введите координаты населенного пункта, например Санкт-Петербург: 59.93, 30.31')
lat = input('Введите широту: ')
lon = input('Введите долготу: ')
def current_weather(lat, lon):

    """
    Описание функции, входных и выходных переменных
    """
    token = '745cf102-b0eb-4191-8306-b28f31dac08e'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"  # Если вдруг используете тариф «Погода на вашем сайте»
    # то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Данная реализация приведена для тарифа «Тестовый», если у вас Тариф «Погода на вашем сайте», то закомментируйте пару строк указанных ниже
    result = {
        'Город': data['geo_object']['locality']['name'],  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        'Время запроса': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        'Температура С': data['fact']['temp'],  # TODO Реализовать вычисление температуры из данных полученных от API
        'Ощущается как С': data['fact']['feels_like'],  # TODO Реализовать вычисление ощущаемой температуры из данных полученных от API
        'Давление ммрст': data['fact']['pressure_mm'],  # TODO Реализовать вычисление давления из данных полученных от API
        'Влажность %': data['fact']['humidity'],  # TODO Реализовать вычисление влажности из данных полученных от API
        'Скорость ветра м/с': data['fact']['wind_speed'],  # TODO Реализовать вычисление скорости ветра из данных полученных от API
        'Скорость порывов м/с': data['fact']['wind_gust'],  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
        'Направление ветра': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
    }
    return result


if __name__ == "__main__":
    print(json.dumps(current_weather(lat, lon), indent=4, ensure_ascii=False))  # Проверка работы для координат Санкт-Петербурга
    print('Координаты некоторых городов: '
          'Москва: 55.75, 37.61  '
          'Санкт-Петербург: 59.93, 30.31 '
          'Владисвосток: 43.13, 131.91 '
          'Новосибирск: 55.03, 82.96 '
          'Сидней: -33.86, 151.20 ' 
          'Будапешт: 47.49, 19.03 '
          )