from django.urls import path, include
from app_weather.views import weather_wiew


urlpatterns = [
    path('weather/', weather_wiew),

]