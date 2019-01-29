"""Test entity application for Words entity """
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.application.words.words import (
    WordsSerializer, WordsDetailSerializer)
from rest_framework.exceptions import ValidationError
from django.test import RequestFactory
from logogram_v1.domain_persistence.users.models import Users
from logogram_v1.domain_persistence.flashcards.models import FlashCards


class WordsSerializerApplication(BaseTestCase):

    def setUp(self):
        super(WordsSerializerApplication, self).setUp()

    def test_raise_validation_error(self):
        """
        Test the raise_validation_error method
            - that when given a none value  it raises a validation error
            - that the tests pass whn the an object is given
        """
        # Passing function
        WordsSerializer().raise_validation_error(object, "request")
        with self.assertRaises(ValidationError):
            WordsSerializer().raise_validation_error(None, "request")

    def test_to_internal_value_success(self):
        """
        Test that data is returned when passed to the to_internal_value method
        """
        Users.objects.create(email="courage@gmail.com", first_name="courage",
                             last_name="the cowardly dog")
        user = Users.objects.get(email="courage@gmail.com")
        FlashCards.objects.create(
            name="Flashcard 1", description="Description1", user=user)
        flashcard = FlashCards.objects.get(name="Flashcard 1")
        request = RequestFactory()
        request.user = user
        request.parser_context = {"kwargs": {"pk": flashcard.pk}}
        data = {"name": "Word 1", "description": "Word Description"}
        retrieved_data = WordsSerializer(
            context={"request": request}).to_internal_value(data)
        self.assertEqual(retrieved_data["name"], data["name"])
        self.assertEqual(retrieved_data["description"], data["description"])
        self.assertEqual(retrieved_data["user"], user)
        self.assertEqual(retrieved_data["flashcard"], flashcard)

    def test_to_internal_value_errors(self):
        """
        Test the validation errors raised on the to_internal_value method
        """
        # do not pass request object
        data = {"name": "Word 1", "description": "Word Description"}
        with self.assertRaises(ValidationError):
            WordsSerializer().to_internal_value(data)
        request = RequestFactory()
        request.user = None
        # pass request without a None user
        with self.assertRaises(ValidationError):
            WordsSerializer(
                context={"request": request}).to_internal_value(data)
        # pass request without flashcard id
        Users.objects.create(email="courage@gmail.com", first_name="courage",
                             last_name="the cowardly dog")
        user = Users.objects.get(email="courage@gmail.com")
        request.user = user
        request.parser_context = {"kwargs": {}}
        with self.assertRaises(ValidationError):
            WordsSerializer(
                context={"request": request}).to_internal_value(data)
        # Pass none existent flashcard
        request.parser_context = {"kwargs": {"pk": 12345}}
        with self.assertRaises(ValidationError):
            WordsSerializer(
                context={"request": request}).to_internal_value(data)


class WordsDetailSerializerApplication(BaseTestCase):

    def setUp(self):
        super(WordsDetailSerializerApplication, self).setUp()

    def test_words_serializer_class(self):
        """
        Test that the Words Serializer class contains the required fields.
        """
        serializer_data = WordsDetailSerializer().data
        self.assertEqual(set(serializer_data.keys()),
                         set(['name', 'description']))
