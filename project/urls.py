"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from random import random
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from app_datetime.views import datetime_wiew
from app_weather.views import my_wiew
from store.views import products_view
from store.views import shop_view

def random_wiew(request):
    return HttpResponse(random())
urlpatterns = [
    path('admin/', admin.site.urls),
    path('random/', random_wiew),
    path('datetime/', datetime_wiew),
    path('weather/', my_wiew),
    path('product/', products_view),
    path('', shop_view),


]

