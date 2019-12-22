from qvsta_server.qvsta_api.serializers.modelUsersSerializer import ModelUsersSerializer
from qvsta_server.qvsta_api.models import ModelUsers
from rest_framework import status, response, mixins, generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
import random
from itertools import chain




class ModelUsersList(generics.ListCreateAPIView):
    queryset = ModelUsers.objects.all()
    serializer_class = ModelUsersSerializer
    filter_backends = (DjangoFilterBackend,)

    
    def model_filter(self, queryset ,MOOD_IMAGE_COUNT, filterValue1, filterValue2 = None, isRating = False):
        if filterValue2 == None and isRating == False:
            filteredQuery = queryset.filter(modellooks__lookTag = filterValue1)
        elif isRating == False:
            filteredQuery = queryset.filter(modeluserdetails__modelDetail = filterValue1, modeluserdetails__value = filterValue2)
        else: 
            filteredQuery = queryset.filter(rating = filterValue1)

        countQuery = filteredQuery.values('modelID').count()
        if countQuery >= MOOD_IMAGE_COUNT:
            return filteredQuery
        elif countQuery < MOOD_IMAGE_COUNT:
            
            valid_id_list = ModelUsers.objects.exclude(modelID__in = filteredQuery).values_list('modelID', flat=True)
            random_list = random.sample(set(valid_id_list), min(len(valid_id_list), MOOD_IMAGE_COUNT - countQuery))
            randomQuery = ModelUsers.objects.filter(modelID__in = random_list)
            finalQuery = filteredQuery | randomQuery
            return finalQuery.distinct()
        
  


    def get_queryset(self):
        
        queryset = ModelUsers.objects.all()

        gender = self.request.query_params.get('gender', None)
        ethnicity = self.request.query_params.get('ethnicity', None)
        hairColor = self.request.query_params.get('hairColor', None)
        
        lookTag1 = self.request.query_params.get('lookTag1', None)
        lookTag2 = self.request.query_params.get('lookTag2', None)
        lookTag3 = self.request.query_params.get('lookTag3', None)
        lookTagList = []

        hairLength = self.request.query_params.get('hairLength', None)

        if lookTag1 is not None:
            lookTagList.append(lookTag1)
        if lookTag2 is not None:
            lookTagList.append(lookTag2)
        if lookTag3 is not None:
            lookTagList.append(lookTag3)

        if gender is not None:
            queryset = queryset.filter(genderID = gender)
        if ethnicity is not None:
            queryset = queryset.filter(modeluserdetails__modelDetail = 'Ethnicity', modeluserdetails__value = ethnicity)
        if hairColor is not None:
            queryset = queryset.filter(modeluserdetails__modelDetail = 'Hair Color', modeluserdetails__value = hairColor)
        
        count = queryset.values("modelID").count()
        MOOD_IMAGE_COUNT = 8

        if count <= MOOD_IMAGE_COUNT:
            return queryset

        #looks filter
        if lookTagList != []:
            for look in lookTagList:
                queryset = self.model_filter(queryset, MOOD_IMAGE_COUNT, look)
        if queryset.values('modelID').count() == MOOD_IMAGE_COUNT:
            return queryset
          
        #hairLength Filter  
        if hairLength is not None:
            queryset = self.model_filter(queryset, MOOD_IMAGE_COUNT, "Hair Length", hairLength)
        if queryset.values('modelID').count() == MOOD_IMAGE_COUNT:
            return queryset

        #filters down by rating
        queryset = self.model_filter(queryset, MOOD_IMAGE_COUNT, filterValue1 = 1, isRating = True)
        if queryset.values('modelID').count() == MOOD_IMAGE_COUNT:
            return queryset

        queryset = self.model_filter(queryset, MOOD_IMAGE_COUNT, filterValue1 = 2, isRating = True)
        if queryset.values('modelID').count() == MOOD_IMAGE_COUNT:
            return queryset
        
        queryset = self.model_filter(queryset, MOOD_IMAGE_COUNT, 3, isRating = True)
        if queryset.values('modelID').count() == MOOD_IMAGE_COUNT:
            return queryset
         
        #insures a random query of 8 is returned at the end 
        if queryset.values('modelID').count() > MOOD_IMAGE_COUNT:
            valid_id_list = queryset.values_list('modelID', flat=True)
            random_list = random.sample(set(valid_id_list), min(len(valid_id_list), MOOD_IMAGE_COUNT))
            queryset = ModelUsers.objects.filter(modelID__in = random_list)
        return queryset.distinct()



#
#   Gender, Ethnicity, Hair Color
#
#   Hairlength
#
#   Tag
#
#   Rating
#