from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import BriefingAgencies

class BriefingAgenciesSerializer(serializers.ModelSerializer):
    """
    Serializer for Briefing Agencies.
    """

    class Meta:
        model = BriefingAgencies
        fields = ('agencyID', 'briefingAgenciesID')

class BriefingAgenciesWithBriefingIDSerializer(serializers.ModelSerializer):
    """
    Serializer for Briefing Agencies.
    """

    class Meta:
        model = BriefingAgencies
        fields = ('agencyID', 'briefingAgenciesID', 'briefingID')


class BriefingAgenciesEmailSerializer(serializers.ModelSerializer):
    """
    Serializer for Briefing Agencies.
    """

    class Meta:
        model = BriefingAgencies
        fields = ('briefingID', 'emailTemplate')

class BriefingDuplicate(serializers.ModelSerializer):
    """
    Serializer for Briefing Agencies.
    """

    class Meta:
        model = BriefingAgencies
        fields = ('briefingID',)