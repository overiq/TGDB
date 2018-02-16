from django.http import HttpResponse
import datetime
from django.shortcuts import render
from django.conf import settings


def index(request):
    return HttpResponse("Hello Django")


def today_is(request):
    now = datetime.datetime.now()
    return render(request, 'blog/datetime.html', {
                                    'now': now,
                                    'template_name': 'blog/nav.html' ,
                                    'base_dir': settings.BASE_DIR }
                                )

