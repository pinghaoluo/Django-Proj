from django.contrib.auth import login, authenticate
from qvsta_server.qvsta_api.serializers.briefingSerializers.briefingsSerializer import BriefingsSerializer
from qvsta_server.qvsta_api.serializers.briefingSerializers.briefingAgenciesSerializer import BriefingDuplicate
from qvsta_server.qvsta_api.models import Briefings, BriefingModelRequests, BriefingAgencies, ModelRequestLooks, ModelRequestDetails, ModelRequestFiles
from rest_framework import status, response, mixins, generics, viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseForbidden



class BriefingsList(generics.ListCreateAPIView):
    queryset = Briefings.objects.all()
    serializer_class = BriefingsSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('status',)
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        briefing = serializer.save()   
                
        briefing.creatingUserID = self.request.user
        briefing.clientID = self.request.user.companyID
        briefing.save()

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Briefings.objects.all()
        queryset = queryset.filter(clientID = self.request.user.companyID.companyID)
        return queryset



class BriefingsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Briefings.objects.all()
    serializer_class = BriefingsSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
       
        briefingID = instance.briefingsID        
        BriefingAgencies.objects.filter(briefingID = briefingID).delete()

        modelRequestIDs = BriefingModelRequests.objects.filter(briefingID = briefingID).values_list('modelRequestID', flat = True)
        modelRequestList = list(set(modelRequestIDs))

        for modelRequest in modelRequestList:
            ModelRequestDetails.objects.filter(modelRequestID = modelRequest).delete()
            ModelRequestLooks.objects.filter(modelRequestID = modelRequest).delete()
            ModelRequestFiles.objects.filter(modelRequestID = modelRequest).delete()

        BriefingModelRequests.objects.filter(briefingID = briefingID).delete()

        Briefings.objects.get(briefingsID = briefingID).delete()        

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        
        return HttpResponseForbidden()

# class BriefingsDuplicate(generics.CreateAPIView):
#     serializer_class = BriefingDuplicate

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         briefing = serializer.validated_data.get('briefingID')      

#         briefing.briefingsID = None

#         briefing.creatingUserID = self.request.user
#         briefing.clientID = self.request.user.companyID
#         briefing.save()
        
#         briefingID = briefing.briefingsID

#         briefingAgenciesID = BriefingAgencies.objects.filter(briefingID = briefing.briefingsID).values_list('briefingAgenciesID', flat = True)
#         briefingAgenciesList = list(set(briefingAgenciesID))

#         for briefingAgency in briefingAgenciesList:
#             briefingAgent = BriefingAgencies.objects.get(briefingAgenciesID = briefingAgency)
#             briefingAgent.briefingAgenciesID = None
#             briefingAgent.save()

#         briefingModelRequestsID = BriefingAgencies.objects.filter(briefingID = briefing.briefingsID).values_list('briefingAgenciesID', flat = True)
#         briefingModelRequestsList = list(set(briefingModelRequestsID))

#         for briefingModelRequest in briefingModelRequestsList:
            



#         headers = self.get_success_headers(serializer.data)

#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)