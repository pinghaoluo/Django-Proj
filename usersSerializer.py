from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from qvsta_server.qvsta_api.models import Users

class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'password', 'companyID', 'userID', 'created', 'lastEdit', 'userType', 'phoneNumber')

    def create(self, validated_data):
        user = super(UsersSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
