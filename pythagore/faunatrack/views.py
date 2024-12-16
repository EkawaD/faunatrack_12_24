
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def bonjour(request):
    return HttpResponse("Bonjour !")