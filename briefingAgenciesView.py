from django.contrib.auth import login, authenticate
from qvsta_server.qvsta_api.serializers.briefingSerializers.briefingAgenciesSerializer import BriefingAgenciesEmailSerializer, BriefingAgenciesSerializer, BriefingAgenciesWithBriefingIDSerializer
from qvsta_server.qvsta_api.models import BriefingAgencies, Companies
from rest_framework import status, response, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.core.mail import send_mail
from django.template.loader import get_template, render_to_string
from django.template import Context

class BriefingsAgenciesList(generics.ListCreateAPIView):
    queryset = BriefingAgencies.objects.all()
    serializer_class = BriefingAgenciesWithBriefingIDSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('briefingID',)

class BriefingsAgenciesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BriefingAgencies.objects.all()
    serializer_class = BriefingAgenciesWithBriefingIDSerializer


class BriefingsAgenciesSendEmail(generics.ListCreateAPIView):
    queryset = BriefingAgencies.objects.all()
    serializer_class = BriefingAgenciesEmailSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('briefingID',)

    def post(self, request, format = None):
        serializer = BriefingAgenciesEmailSerializer(data=request.data)

        if serializer.is_valid() == False:
            print("invalid input")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if BriefingAgencies.objects.filter(briefingID = serializer.initial_data.get('briefingID')).exists():
            briefingID = serializer.initial_data.get('briefingID')
        else:
            print("briefingID doesn't exist")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        agencyIDs = BriefingAgencies.objects.filter(briefingID = briefingID).values_list('agencyID', flat = True)
        agencyList = list(set(agencyIDs))
        emailList = []
        for agency in agencyList:
            emailList.append(Companies.objects.get(companyID = agency).email)
        print("valid or resending")
       
        print(serializer.initial_data.get('email'))
        print(serializer.initial_data.get('uniqueID'))

        for agency in agencyList:
            subject = "TEST FOR BRIEFINGAGENCIES"
            from1 = 'info@qvsta.com'

            send_mail(
                subject,
                'Hello',
                from1,
                [Companies.objects.get(companyID = agency).email],
                fail_silently=False,
                html_message= BriefingAgencies.objects.get(agencyID = agency, briefingID = briefingID).emailTemplate
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
