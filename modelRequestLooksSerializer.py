from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import ModelRequestLooks, Looks
from qvsta_server.qvsta_api.serializers.briefingSerializers import looksSerializer

class ModelRequestLooksSerializer(serializers.ModelSerializer):
    """
    Serializer for ModelRequestLooks.
    """
    
    class Meta:
        model = ModelRequestLooks
        fields = ('lookTag', 'freeText',)

  