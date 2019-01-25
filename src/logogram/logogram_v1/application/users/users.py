from logogram_v1.domain_persistence.users.models import Users
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email')
