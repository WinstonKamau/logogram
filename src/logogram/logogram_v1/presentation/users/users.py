from logogram_v1.domain_persistence.users.models import Users
from logogram_v1.application.users.users import UsersSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404


class UsersView(generics.ListCreateAPIView):
    """
    List all users in the application
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user.
    """
    serializer_class = UsersSerializer
    queryset = Users.objects.all()
