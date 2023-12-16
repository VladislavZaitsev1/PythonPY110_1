from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# Create your views here.


def datetime_wiew(request):
    if request.method == 'GET':
        return HttpResponse(datetime.now())