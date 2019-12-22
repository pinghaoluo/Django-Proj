from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import ModelDetails

class ModelDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for ModelDetails.
    """
    class Meta:
        model = ModelDetails
        fields = ('modelDetail',)

  