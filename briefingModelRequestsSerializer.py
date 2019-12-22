from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import BriefingModelRequests, ModelRequestDetails, ModelRequestFiles, ModelRequestLooks
from qvsta_server.qvsta_api.serializers.briefingSerializers import modelRequestDetailsSerializer, modelRequestFilesSerializer, modelRequestLooksSerializer
from collections import OrderedDict
from rest_framework.fields import SkipField


class BriefingModelRequestsSerializer(serializers.ModelSerializer):
    """
    Serializer for BriefingModelRequests.
    """
    modelRequestDetails = modelRequestDetailsSerializer.ModelRequestDetailsSerializer(many=True, required = False)
    modelRequestFiles =  modelRequestFilesSerializer.ModelRequestFilesSerializer(many=True, required = False)
    modelRequestLooks =  modelRequestLooksSerializer.ModelRequestLooksSerializer(many=True, required = False)   

    class Meta:
        model = BriefingModelRequests
        fields = ('modelRequestID', 'genderID', 'fromAge', 'toAge', 'modelRequestFiles', 'modelRequestDetails',  'modelRequestLooks',)

    def create(self, validated_data, briefingID = None):
        modelRequestDetails = None
        modelRequestLooks = None
        modelRequestFiles = None

        if 'modelRequestDetails' in validated_data:
            modelRequestDetails = validated_data.pop('modelRequestDetails')
        if 'modelRequestLooks' in validated_data:
            modelRequestLooks = validated_data.pop('modelRequestLooks')
        if 'modelRequestFiles' in validated_data:
            modelRequestFiles = validated_data.pop('modelRequestFiles')
      
        if (briefingID == None):
            briefingModelRequests = BriefingModelRequests.objects.create(**validated_data)
        else:
            briefingModelRequests = BriefingModelRequests.objects.create(**validated_data, briefingID = briefingID)

        if modelRequestDetails is not None:
            for data in modelRequestDetails:
                ModelRequestDetails.objects.create(modelRequestID = briefingModelRequests, **data)
        if modelRequestLooks is not None:
            for data in modelRequestLooks:
                ModelRequestLooks.objects.create(modelRequestID = briefingModelRequests, **data)
        if modelRequestFiles is not None:
            for data in modelRequestFiles:
                ModelRequestFiles.objects.create(modelRequestID = briefingModelRequests, **data)

        return briefingModelRequests


class BriefingModelRequestsWithBriefingIDSerializer(serializers.ModelSerializer):
    """
    Serializer for BriefingModelRequests.
    """
    class Meta:
        model = BriefingModelRequests
        fields = ('briefingID', 'modelRequestID', 'genderID', 'fromAge', 'toAge', 'modelRequestFiles', 'modelRequestDetails',  'modelRequestLooks',)