from rest_framework import serializers
from faunatrack.models import Espece, Observation

class EspeceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espece
        fields = "__all__"

class EspeceSerializerObservation(serializers.ModelSerializer):
    class Meta:
        model = Espece
        fields = ["nom"]


class ObservationSerializer(serializers.ModelSerializer):

    espece = EspeceSerializer(read_only=True)

    class Meta:
        model = Observation
        fields = "__all__"

    def validate_notes(self, value):
        """
        Check that the notes is about Django.
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Notes is not about Django")
        return value