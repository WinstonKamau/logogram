"""Test entity application user cases of the FlashCards entity """
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.application.flashcards.flashcards import FlashCardsSerializer
from logogram_v1.domain_persistence.users.models import Users
from logogram_v1.domain_persistence.flashcards.models import FlashCards
from django.test import RequestFactory
from rest_framework.exceptions import ValidationError


class FlashCardsSerializerApplication(BaseTestCase):

    def setUp(self):
        Users.objects.create(
            email="buttercup@gmail.com", first_name="Butter", last_name="Cup")
        self.user = Users.objects.get(email="buttercup@gmail.com")
        self.request = RequestFactory()
        self.request.user = self.user
        super(FlashCardsSerializerApplication, self).setUp()

    def test_flash_card_name_length(self):
        """
        Test that the name attribute of a flash card will raise an invalid
        an invalid attribute when:
            - The length of the name is greater than thirty characters.
        """
        serializer_data = FlashCardsSerializer().data
        normal_name_length = "Short name"
        description = "Short description"
        serializer_data['name'] = normal_name_length
        serializer_data['description'] = description
        serializer = FlashCardsSerializer(data=serializer_data,
                                          context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        long_name_length = "aflashcardnamegreatherthanthirtycharacters"
        serializer_data_2 = FlashCardsSerializer().data
        serializer_data_2['name'] = long_name_length
        serializer_data_2['description'] = description
        serializer_2 = FlashCardsSerializer(data=serializer_data_2)
        self.assertFalse(serializer_2.is_valid())
        name_error_message = ('Ensure this field has no more than '
                              '30 characters.')
        self.assertIn(name_error_message, serializer_2.errors["name"])
        self.assertIsNone(serializer_2.errors.get("description"))

    def test_flash_card_attributes_blank(self):
        """
        Test that the name attribute on a FlashCards Serializer will:
            - raise an invalid attribute when the name attribute is blank
            - not raise an error when the description is blank
        """
        serializer_data = FlashCardsSerializer().data
        serializer_data['name'] = ""
        serializer_data['description'] = ""
        serializer = FlashCardsSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        blank_error_message = "This field may not be blank."
        self.assertIn(blank_error_message, serializer.errors["name"])
        self.assertIsNone(serializer.errors.get("description"))

    def test_automatically_added_attributes(self):
        """
        Test that the user, creation and modification date of a flash card
        exists or is automatically created when creating a Flash Card.
        """
        serializer_data = FlashCardsSerializer().data
        serializer_data['name'] = "Flash Card 1"
        serializer_data['description'] = "Short Description"
        serializer = FlashCardsSerializer(data=serializer_data,
                                          context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        flash_card = FlashCards.objects.get(name="Flash Card 1")
        self.assertIsNotNone(flash_card.creation_date)
        self.assertIsNotNone(flash_card.modification_date)
        self.assertEqual(flash_card.user.email, self.user.email)

    def test_validation_error_without_request(self):
        """
        Test that if you post data to the serializer class without a request
        object
            - That a validation error is raised
        """
        serializer_data = FlashCardsSerializer().data
        serializer_data['name'] = "Flash Card 1"
        serializer_data['description'] = "Short Description"
        serializer = FlashCardsSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        request_error_message = ('No request object was used to access'
                                 ' the view')
        self.assertIn(request_error_message, serializer.errors["user"])

    def test_validation_error_for_request_without_user(self):
        """
        Test that if you post data to the serializer class with a request
        object that does not have a user attribute
            - That a validation error is raised
        """
        serializer_data = FlashCardsSerializer().data
        serializer_data['name'] = "Flash Card 1"
        serializer_data['description'] = "Short Description"
        request = RequestFactory()
        request.user = None
        serializer = FlashCardsSerializer(data=serializer_data,
                                          context={"request": request})
        self.assertFalse(serializer.is_valid())
        request_error_message = "This field is required."
        self.assertIn(request_error_message, serializer.errors["user"])

    def test_no_request_submitted_to_internal_value(self):
        """
        Test that a request is not submitted to the to_internal_value method
        """
        data = {"name": "Flash Card 1", "description": "Card Description"}
        serializer = FlashCardsSerializer()
        with self.assertRaises(ValidationError):
            serializer.to_internal_value(data)

    def test_user_not_submitted_to_internal_value(self):
        """
        Test that a request is not submitted to the to_internal_value method
        """
        data = {"name": "Flash Card 1", "description": "Card Description"}
        Users.objects.create(first_name="Professor", last_name="Utonium",
                             email="utonium@gmail.com")
        request = RequestFactory()
        request.user = None
        serializer = FlashCardsSerializer(context={"request": request})
        with self.assertRaises(ValidationError):
            serializer.to_internal_value(data)

    def test_successful_to_internal_value(self):
        """
        Test the internal_value_method
        """
        data = {"name": "Flash Card 1", "description": "Card Description"}
        Users.objects.create(first_name="Professor", last_name="Utonium",
                             email="utonium@gmail.com")
        user = Users.objects.get(email="utonium@gmail.com")
        request = RequestFactory()
        request.user = user
        serializer = FlashCardsSerializer(context={"request": request})
        self.assertIn(data["name"], serializer.to_internal_value(data)["name"])
        self.assertIn(data["description"],
                      serializer.to_internal_value(data)["description"])


class FlashCardsDetailSerializerApplication(BaseTestCase):

    def setUp(self):
        Users.objects.create(
            email="buttercup@gmail.com", first_name="Butter", last_name="Cup")
        self.user = Users.objects.get(email="buttercup@gmail.com")
        self.request = RequestFactory()
        self.request.user = self.user
        super(FlashCardsDetailSerializerApplication, self).setUp()

    def test_create_new_flashcard(self):
        """
        Test that a flash card can be added
        """
        serializer_data = FlashCardsSerializer().data
        normal_name_length = "Short name"
        description = "Short description"
        serializer_data['name'] = normal_name_length
        serializer_data['description'] = description
        serializer = FlashCardsSerializer(data=serializer_data,
                                          context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        flash_card = FlashCards.objects.get(name="Short name")
        self.assertIsNotNone(flash_card)
