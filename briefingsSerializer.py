from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import Briefings, BriefingAgencies, BriefingModelRequests, ModelRequestDetails, ModelRequestFiles, ModelRequestLooks
from qvsta_server.qvsta_api.serializers.briefingSerializers import briefingModelRequestsSerializer, briefingAgenciesSerializer
from drf_writable_nested import WritableNestedModelSerializer, NestedCreateMixin
from collections import OrderedDict
from rest_framework.fields import SkipField

class BriefingsSerializer(serializers.ModelSerializer):
    """
    Serializer for Briefings.
    """
    briefingAgencies = briefingAgenciesSerializer.BriefingAgenciesSerializer(many = True, required = False)
    briefingModelRequests = briefingModelRequestsSerializer.BriefingModelRequestsSerializer(many = True, required = False)

    class Meta:
        model = Briefings
        fields = ('briefingsID', 'title', 'description','fromDate', 'toDate', 'commentDate'
        , 'country', 'state', 'city', 'street','zipCode', 'payRate', 'commentPayRate'
        , 'buyOuts', 'commentBuyOuts', 'travelFee', 'commentTravel', 'briefingAgencies', 'briefingModelRequests')

    
    def create(self, validated_data):
        briefingAgencies1 = None
        briefingModelRequests1 = None

        if 'briefingAgencies' in validated_data:
            briefingAgencies1 = validated_data.pop('briefingAgencies')

        if 'briefingModelRequests' in validated_data:
            briefingModelRequests1 = validated_data.pop('briefingModelRequests')
      
        briefings = Briefings.objects.create(**validated_data)
       
        if briefingAgencies1 is not None:
            for data in briefingAgencies1:
                BriefingAgencies.objects.create(briefingID = briefings, **data)
        if briefingModelRequests1 is not None:
            for data in briefingModelRequests1:
                serializer = briefingModelRequestsSerializer.BriefingModelRequestsSerializer(data = data)
                serializer.create(data, briefingID = briefings)
            
        return briefings


    def delete_briefing_agencies(self, briefingID, currentBriefingAgencies):
        IDs = BriefingAgencies.objects.filter(briefingID = briefingID).values_list('agencyID', flat = True)
        List = list(set(IDs))
        List1 = [] 
    
        for briefing in currentBriefingAgencies:
            List1.append(briefing.get('agencyID', None).companyID)

        for agency in List:
            if agency not in List1:
                BriefingAgencies.objects.filter(briefingID = briefingID, agencyID = agency).delete()
        
    def update_briefing_agencies(self, briefings, currentBriefingAgencies):
        if currentBriefingAgencies:
            for briefingAgency_data in currentBriefingAgencies:
                agencyID = briefingAgency_data.get('agencyID', None)
                if BriefingAgencies.objects.filter(agencyID = agencyID, briefingID = briefings.briefingsID).exists():
                    briefingAgency = BriefingAgencies.objects.get(agencyID = agencyID, briefingID = briefings.briefingsID)
                    briefingAgency.agencyID = briefingAgency_data.get('agencyID', briefingAgency.agencyID)
                    briefingAgency.briefingAgenciesID = briefingAgency_data.get('briefingAgenciesID', briefingAgency.briefingAgenciesID)
                    briefingAgency.save()
                else:
                    BriefingAgencies.objects.create(briefingID = briefings, **briefingAgency_data)

    def update_briefing_model_requests(self, briefings, currentBriefingModelRequests):

        modelRequestIDs = BriefingModelRequests.objects.filter(briefingID = briefings.briefingsID).values_list('modelRequestID', flat = True)
        modelRequestList = list(set(modelRequestIDs))

        for modelRequest in modelRequestList:
            ModelRequestDetails.objects.filter(modelRequestID = modelRequest).delete()
            ModelRequestFiles.objects.filter(modelRequestID = modelRequest).delete()
            ModelRequestLooks.objects.filter(modelRequestID = modelRequest).delete()
            BriefingModelRequests.objects.filter(briefingID = briefings.briefingsID, modelRequestID = modelRequest).delete()
    
        if currentBriefingModelRequests:
            for briefingModelRequest_data in currentBriefingModelRequests:
                    serializer = briefingModelRequestsSerializer.BriefingModelRequestsSerializer(data = briefingModelRequest_data)
                    serializer.create(briefingModelRequest_data, briefingID = briefings)

    def update(self, instance, validated_data):
        briefingAgencies1 = None
        briefingModelRequests1 = None

        if 'briefingAgencies' in validated_data:
            briefingAgencies1 = validated_data.pop('briefingAgencies')

        if 'briefingModelRequests' in validated_data:
            briefingModelRequests1 = validated_data.pop('briefingModelRequests')
    
        briefings = super(BriefingsSerializer, self).update(instance, validated_data)
        briefingID = briefings.briefingsID

        self.delete_briefing_agencies(briefingID, briefingAgencies1)

        self.update_briefing_agencies(briefings, briefingAgencies1)

        self.update_briefing_model_requests(briefings, briefingModelRequests1)
        
        return instance

        
