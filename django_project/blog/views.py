from django.http import HttpResponse
import datetime
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello Django")


def today_is(request):
    now = datetime.datetime.now()
    return render(request, 'blog/datetime.html', {'now': now })
