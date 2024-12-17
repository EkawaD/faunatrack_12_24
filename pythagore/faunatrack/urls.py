from django.urls import path
from faunatrack.views import ObservationCreate, faunatrack_home, observation_list, ObservationList, ProjetList

urlpatterns = [
    path("",  faunatrack_home, name="faunatrack_home"),
    path("projets/", ProjetList.as_view(),  name="projet_list"),
    path("observations/", ObservationList.as_view(),  name="observation_list"),
    path("observations/add/", ObservationCreate.as_view(), name="observation_create")
]
