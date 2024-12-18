from rest_framework import viewsets, views, response
from faunatrack.models import Observation
from faunatrack.serializers import ObservationSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated



class ObservationViewset(viewsets.ModelViewSet):
    
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    permission_classes = [IsAuthenticated]


class ExampleView(views.APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return response.Response(content)