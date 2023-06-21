from django.shortcuts import render
from django.http import HttpResponse
from django_server import settings

# Create your views here.
def index(request):
    key = settings.SECRET_KEY
    return HttpResponse("Hello! Django World! " + key)