from django.contrib.auth import login, authenticate
from qvsta_server.qvsta_api.serializers.briefingSerializers.briefingModelRequestsSerializer import BriefingModelRequestsSerializer, BriefingModelRequestsWithBriefingIDSerializer
from qvsta_server.qvsta_api.models import BriefingModelRequests
from rest_framework import status, response, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class BriefingModelRequestsList(generics.ListCreateAPIView):
    queryset = BriefingModelRequests.objects.all()
    serializer_class = BriefingModelRequestsWithBriefingIDSerializer
   
class BriefingModelRequestsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BriefingModelRequests.objects.all()
    serializer_class = BriefingModelRequestsWithBriefingIDSerializer


