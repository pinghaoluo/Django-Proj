from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import Looks

class LooksSerializer(serializers.ModelSerializer):
    """
    Serializer for Looks.
    """
    class Meta:
        model = Looks
        fields = ('lookTag',)

    


