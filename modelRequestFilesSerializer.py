from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import ModelRequestFiles

class ModelRequestFilesSerializer(serializers.ModelSerializer):
    """
    Serializer for ModelRequestDetails.
    """
    class Meta:
        model = ModelRequestFiles
        fields = ('modelRequestID', 'fileID')

    