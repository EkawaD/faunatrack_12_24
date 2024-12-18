from rest_framework import viewsets, views, response
from faunatrack.models import Observation
from faunatrack.serializers import ObservationSerializer


class ObservationViewset(viewsets.ModelViewSet):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer


class ExampleView(views.APIView):

    def get(self, request, format=None):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return response.Response(content)