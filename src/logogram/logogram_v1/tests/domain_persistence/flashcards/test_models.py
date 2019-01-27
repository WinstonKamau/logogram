""" Test the domain_persistence of the entitiy flashcard"""
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.domain_persistence.flashcards.models import FlashCards
from logogram_v1.domain_persistence.users.models import Users


class FlashCardsModel(BaseTestCase):

    def setUp(self):
        super(FlashCardsModel, self).setUp()

    def test_flashcard_returned_to_string(self):
        """
        Test that the flashcard object returned when returned as a string it
        gives the name of the flashcard
        """
        Users.objects.create(email="tweety@gmail.com", first_name="tweety",
                             last_name="bird")
        user = Users.objects.get(email="tweety@gmail.com")
        FlashCards.objects.create(name="FlashCard 1", user=user,
                                  description="Description1")
        flash_card = FlashCards.objects.get(name="FlashCard 1")
        self.assertEqual("FlashCard 1", str(flash_card))
