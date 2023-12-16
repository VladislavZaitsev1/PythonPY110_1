from django.shortcuts import render
from weather_api import current_weather
from django.http import JsonResponse
# Create your views here.
def my_wiew(request):
    if request.method == "GET":
        data = {"Город": "Санкт-Петербург",
    "Время запроса": "20:59",
    "Температура С": -1,
    "Ощущается как С": -6,
    "Давление ммрст": 758,
    "Влажность %": 93,
    "Скорость ветра м/с": 4.2,
    "Скорость порывов м/с": 6.9,
    "Направление ветра": "южное"}
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})