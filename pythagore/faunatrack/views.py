
from django.http import HttpResponse
from django.shortcuts import render

from faunatrack.models import Espece

# Create your views here.
def bonjour(request):
    print(Espece.objects.all().first())
    return HttpResponse("Bonjour !")