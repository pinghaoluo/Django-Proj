from rest_framework import permissions
from qvsta_server.qvsta_api.models import Users
from rest_framework.filters import SearchFilter

class CompanyDetailPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = 'This authentication is not valid'

    def has_permission(self, request, view, *args, **kwargs):

        try:
            request_company = int(request.resolver_match.kwargs.get('pk'))

            if (request.user.companyID.companyID == request_company and request.user.is_superuser):
                return True
            else:
                return message
        except Exception as e:
            return False