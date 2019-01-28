from logogram_v1.domain_persistence.words.models import Words
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from logogram_v1.domain_persistence.flashcards.models import FlashCards


class WordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Words
        fields = ('name', 'description')
        validation_errors = {"request": {
            'user': 'No request object was used to access the view'},
            "request_user": {'user': 'This field is required.'},
            "flashcard_pk": {'flashcard': 'This field is required'},
            "flashcard": {'flashcard': 'This flash card does not exist'}}

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        request = self.context.get("request")
        self.raise_validation_error(request, "request")
        self.raise_validation_error(request.user, "request_user")
        flashcard_pk = request.parser_context.get("kwargs").get("pk")
        self.raise_validation_error(flashcard_pk, "flashcard_pk")
        flashcard = FlashCards.objects.filter(id=flashcard_pk).first()
        self.raise_validation_error(flashcard, "flashcard")
        data.update({'user': request.user, 'flashcard': flashcard})
        return data

    def raise_validation_error(self, data_object, data_string):
        if not data_object:
            raise ValidationError(self.Meta.validation_errors.get(
                data_string))
