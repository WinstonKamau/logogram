from logogram_v1.domain_persistence.flashcards.models import FlashCards
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class FlashCardsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlashCards
        fields = ('name', 'description')

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        request = self.context.get("request")
        if not request:
            raise ValidationError({
                'user': 'No request object was used to access the view'
            })
        if not request.user:
            raise ValidationError({
                'user': 'This field is required.'
            })
        data.update({'user': request.user})
        return data


class FlashCardsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlashCards
        fields = ('name', 'description')
