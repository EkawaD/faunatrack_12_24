from django.urls import path, include
from faunatrack.views import ObservationCreate, faunatrack_home, ObservationDelete,  ObservationDetail, ObservationUpdate, ObservationList, ProjetList
import faunatrack.api_views as api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"observations", api.ObservationViewset) #/faunatrack/api/observations/


urlpatterns = [
    path("",  faunatrack_home, name="faunatrack_home"),
    path("projets/", ProjetList.as_view(),  name="projet_list"),
    path("observations/", ObservationList.as_view(),  name="observation_list"),
    path("observations/add/", ObservationCreate.as_view(), name="observation_create"),
    path("observations/<int:pk>/", ObservationDetail.as_view(), name="observation_detail"),
    path("observations/edit/<int:pk>/", ObservationUpdate.as_view(), name="observation_update"),
    path("observations/delete/<int:pk>/", ObservationDelete.as_view(), name="observation_delete"),
    path("example/", api.ExampleView.as_view(), name="example"),
    path("api/", include(router.urls)) 
]
