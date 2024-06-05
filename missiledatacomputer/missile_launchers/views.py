from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

def index(request):
    return HttpResponse("Missile Launchers application is online. Route is accessible")