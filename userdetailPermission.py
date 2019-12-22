from rest_framework import permissions
from qvsta_server.qvsta_api.models import Users
from rest_framework.filters import SearchFilter
from django.contrib.auth.hashers import check_password
import json
class UserDetailPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
     
    def has_permission(self, request, view, *args, **kwargs):
        try:
            request_user = int(request.resolver_match.kwargs.get('pk'))
            received_json_data = json.loads(request.body.decode("utf-8"))
            if check_password(received_json_data['password'], request.user.password):

                if (request.user.userID != request_user ):
                    raise Exception

                else:
                    return True
            else:
                raise Exception
                    
        except Exception as e:
            return False
            