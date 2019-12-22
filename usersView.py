from django.contrib.auth import login, authenticate
from qvsta_server.qvsta_api.serializers.usersSerializer import UsersSerializer
from qvsta_server.qvsta_api.models import Users, Invitations
from rest_framework import status, response, mixins, generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from qvsta_server.qvsta_api.permission.userdetailPermission import UserDetailPermission
from qvsta_server.qvsta_api.permission.userListPermission import IsPostOrIsAuthenticated


class UsersList(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('companyID',)
    permission_classes = (IsPostOrIsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save() 

        if Invitations.objects.filter(email = user.email).exists():
            user.companyID = Invitations.objects.get(email = user.email).invitingUserID.companyID
        user.save()

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        
        if self.request.user.userID:
            queryset = Users.objects.all()  
            queryset = queryset.filter(userID = self.request.user.userID)
            return queryset
       

class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (UserDetailPermission,)

    queryset = Users.objects.all()
    serializer_class = UsersSerializer

