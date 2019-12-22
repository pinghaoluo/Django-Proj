from django.contrib.auth import login, authenticate
from qvsta_server.qvsta_api.serializers.briefingSerializers.modelRequestLooksSerializer import ModelRequestLooksSerializer
from qvsta_server.qvsta_api.models import ModelRequestLooks
from rest_framework import status, response, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class ModelRequestLooksList(generics.ListCreateAPIView):
    queryset = ModelRequestLooks.objects.all()
    serializer_class = ModelRequestLooksSerializer
   
class ModelRequestLooksDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ModelRequestLooks.objects.all()
    serializer_class = ModelRequestLooksSerializer


