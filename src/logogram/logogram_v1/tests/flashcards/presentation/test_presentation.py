"""Test entity presentation of the FlashCards entity """
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.domain_persistence.users.models import Users
from logogram_v1.domain_persistence.flashcards.models import FlashCards
from logogram_v1.presentation.flashcards.flashcards import (
    FlashCardsView, FlashCardsDetailView)
from django.test import RequestFactory


class FlashCardsViewPresentation(BaseTestCase):

    def setUp(self):
        super(FlashCardsViewPresentation, self).setUp()

    def test_permissions_required(self):
        """
        Test that a user requires to be authenticated in order to access the
        flash cards view page
        """
        response = self.client.get("/api/v1/flashcards/")
        authentication_error = "Authentication credentials were not provided"
        self.assertEqual(response.status_code, 403)
        self.assertIn(authentication_error, response.content.decode("utf-8"))
        data = {"name": "Flash Card 1", "description": "Card Description"}
        post_response = self.client.post("/api/v1/flashcards/", data=data)
        authentication_error = "Authentication credentials were not provided"
        self.assertEqual(post_response.status_code, 403)
        self.assertIn(authentication_error,
                      post_response.content.decode("utf-8"))

    def test_get_flashcard_for_particular_user(self):
        """
        Test that a get request to the flashcards URL will only return flash
        cards for a particular user and not for other users.
        """
        Users.objects.create(email="timon@gmail.com", first_name="timon",
                             last_name="pumba")
        Users.objects.create(email="homer@gmail.com", first_name="homer",
                             last_name="simpsons")
        timon = Users.objects.get(email="timon@gmail.com")
        homer = Users.objects.get(email="homer@gmail.com")
        FlashCards.objects.create(name="Flash Card 1", user=timon,
                                  description="Card  1 Description")
        FlashCards.objects.create(name="Flash Card 2", user=homer,
                                  description="Card 2 Description")
        self.client.force_login(timon)
        flash_cards = self.client.get("/api/v1/flashcards/")
        self.assertIn("Flash Card 1", flash_cards.content.decode("utf-8"))
        self.assertIn("Card  1 Description",
                      flash_cards.content.decode("utf-8"))
        self.assertNotIn("Flash Card 2", flash_cards.content.decode("utf-8"))
        self.assertNotIn("Card 2 Description",
                         flash_cards.content.decode("utf-8"))
        self.client.logout()
        forbidden_reponse = self.client.get("/api/v1/flashcards/")
        self.assertEqual(forbidden_reponse.status_code, 403)
        self.client.force_login(homer)
        flash_cards_2 = self.client.get("/api/v1/flashcards/")
        self.assertNotIn("Flash Card 1",
                         flash_cards_2.content.decode("utf-8"))
        self.assertNotIn("Card  1 Description",
                         flash_cards_2.content.decode("utf-8"))
        self.assertIn("Flash Card 2",
                      flash_cards_2.content.decode("utf-8"))
        self.assertIn("Card 2 Description",
                      flash_cards_2.content.decode("utf-8"))

    def test_get_queryset(self):
        """
        Test that the get_queryset method for flashcards returns the
        flashcards of a particuar user.
        """
        Users.objects.create(
            email="buttercup@gmail.com", first_name="Butter", last_name="Cup")
        self.user = Users.objects.get(email="buttercup@gmail.com")
        FlashCards.objects.create(name="Flash Card 1", user=self.user,
                                  description="Card  1 Description")
        flash_card = FlashCards.objects.get(name="Flash Card 1")
        self.request = RequestFactory()
        self.request.user = self.user
        data = FlashCardsView.get_queryset(self)
        self.assertEqual(flash_card, data[0])

    def test_post_flashcard_for_particular_user(self):
        """
        Test that you can post a flashcard and that it is saved in the
        database
        """
        data = {"name": "Flash Card 3", "description": "Card Description 3"}
        Users.objects.create(email="timon@gmail.com", first_name="timon",             
                             last_name="pumba")
        Users.objects.create(email="homer@gmail.com", first_name="homer",
                             last_name="simpsons")
        timon = Users.objects.get(email="timon@gmail.com")
        self.client.force_login(timon)
        flash_cards = self.client.post("/api/v1/flashcards/", data=data)
        self.assertEqual(flash_cards.status_code, 201)
        flash_card = FlashCards.objects.filter(name="Flash Card 3").first()
        self.assertEqual(flash_card.name, data["name"])


class FlashCardsDetailViewPresentation(BaseTestCase):

    def setUp(self):
        Users.objects.create(
            email="buttercup@gmail.com", first_name="Butter", last_name="Cup")
        self.buttercup = Users.objects.get(email="buttercup@gmail.com")
        FlashCards.objects.create(name="Flash Card 1", user=self.buttercup,
                                  description="Card  1 Description")
        self.flash_card = FlashCards.objects.get(name="Flash Card 1")
        super(FlashCardsDetailViewPresentation, self).setUp()

    def test_permissions_required(self):
        """
        Test that permissions are required on the FlashCardsDetailView
        """
        response = self.client.get(
            "/api/v1/flashcards/{}/".format(self.flash_card.id))
        authentication_error = "Authentication credentials were not provided"
        self.assertEqual(response.status_code, 403)
        self.assertIn(authentication_error, response.content.decode("utf-8"))
        data = {"name": "Flash Card 3", "description": "Card Description 3"}
        post_response = self.client.post(
            "/api/v1/flashcards/{}/".format(self.flash_card.id), data=data)
        authentication_error = "Authentication credentials were not provided"
        self.assertEqual(post_response.status_code, 403)
        self.assertIn(authentication_error,
                      post_response.content.decode("utf-8"))

    def test_get_particular_flashcard(self):
        """
        Test the retrieval of a particular flash card.
        """
        self.client.force_login(self.buttercup)
        response = self.client.get(
            "/api/v1/flashcards/{}/".format(self.flash_card.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.flash_card.name, response.content.decode("utf-8"))

    def test_get_queryset(self):
        """
        Test the get_queryset method of the FlashCardsDetailView returns an
        accurate queryset
        """
        self.request = RequestFactory()
        self.request.user = self.buttercup
        self.kwargs = {"pk": self.flash_card.id}
        data = FlashCardsDetailView.get_queryset(self)
        self.assertEqual(self.flash_card, data[0])

    def test_put_request_flash_card(self):
        """
        Test the put request can edit a particular flash card to another name
        """
        self.client.force_login(self.buttercup)
        data = {"name": "Edited Flash Card",
                "description": "Edited Description"}
        put_response = self.client.put(
            "/api/v1/flashcards/{}/".format(self.flash_card.id),
            data, content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        edited_flash_card = FlashCards.objects.get(id=self.flash_card.id)
        self.assertEqual(edited_flash_card.name, data["name"])
        self.assertEqual(edited_flash_card.description, data["description"])

    def test_delete_request_flashcard(self):
        """
        Test the delete request can delete a particular flashcard
        """
        self.client.force_login(self.buttercup)
        before_delete_flash_card = FlashCards.objects.filter(
            name=self.flash_card.name).first()
        self.assertIsNotNone(before_delete_flash_card)
        self.client.delete(
            "/api/v1/flashcards/{}/".format(self.flash_card.id))
        after_delete_flash_card = FlashCards.objects.filter(
            name=self.flash_card.name).first()
        self.assertIsNone(after_delete_flash_card)
