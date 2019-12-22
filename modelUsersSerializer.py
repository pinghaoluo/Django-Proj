from rest_framework import serializers
from qvsta_server.qvsta_api.models import ModelUsers

class ModelUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelUsers
        fields = ('modelID', 'genderID', 'profileImage')
 

