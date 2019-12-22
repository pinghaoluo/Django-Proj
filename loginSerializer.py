from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import Users

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ( 'email', 'password' )




