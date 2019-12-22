from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import ModelRequestDetails
from qvsta_server.qvsta_api.serializers.briefingSerializers import modelDetailsSerializer


class ModelRequestDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for ModelRequestDetails.
    """
    class Meta:
        model = ModelRequestDetails
        fields = ( 'modelDetail', 'value',)

