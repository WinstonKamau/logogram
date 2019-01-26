from logogram_v1.domain_persistence.users.models import Users
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = super().save()
        user.set_password(self.validated_data['password'])
        user.save()
        return user
