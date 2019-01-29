from logogram_v1.domain_persistence.users.models import Users
from logogram_v1.application.users.users import UsersSerializer
from rest_framework import generics
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


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
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersSerializer

    def get_queryset(self):
        """
        This view should return a the details of a user who has logged in
        """
        user = self.request.user
        self.check_pk_similar_to_user_id(user.id, self.kwargs["pk"])
        return Users.objects.filter(id=user.id)

    def check_pk_similar_to_user_id(self, user_id, url_pk):
        """
        Check that the argument passed to the URL is similar to the user's
        id, otherwise raise a PermissionRequired error, as the path is
        forbidden
        """
        if user_id != int(url_pk):
            raise PermissionDenied()
