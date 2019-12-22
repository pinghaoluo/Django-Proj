from qvsta_server.qvsta_api.serializers.briefingSerializers.modelRequestFilesSerializer import ModelRequestFilesSerializer
from qvsta_server.qvsta_api.models import ModelRequestFiles
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

class ModelRequestFilesList(generics.ListCreateAPIView):
    queryset = ModelRequestFiles.objects.all()
    serializer_class = ModelRequestFilesSerializer
   
class ModelRequestFilesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ModelRequestFiles.objects.all()
    serializer_class = ModelRequestFilesSerializer


