from django.urls import path
from faunatrack.views import faunatrack_home

urlpatterns = [
    path("",  faunatrack_home, name="faunatrack_home")
]
