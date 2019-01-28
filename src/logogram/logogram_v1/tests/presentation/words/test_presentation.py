"""Test presentation of the Words entity """
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.presentation.words.words import WordsView
from rest_framework.exceptions import PermissionDenied
from logogram_v1.domain_persistence.users.models import Users
from logogram_v1.domain_persistence.flashcards.models import FlashCards
from django.test import RequestFactory
from logogram_v1.domain_persistence.words.models import Words


class WordsViewPresentation(BaseTestCase):

    def setUp(self):
        Users.objects.create(
            email="mojojojo@gmail.com", first_name="mojo", last_name="jojo")
        self.user = Users.objects.get(email="mojojojo@gmail.com")
        FlashCards.objects.create(
            name="FlashCard1", description="Description1", user=self.user)
        self.flashcard = FlashCards.objects.get(name="FlashCard1")
        super(WordsViewPresentation, self).setUp()

    def test_forbidden_error_get_queryset(self):
        """
        Test that a Permission Denied error is raised by calling the
        get_queryset method, if the flashcard does not exist
        """
        request = RequestFactory()
        request.user = self.user
        world_view = WordsView()
        world_view.request = request
        world_view.kwargs = {"pk": 123456}
        Words.objects.create(
            name="Word 1", description="Description 1", user=self.user,
            flashcard=self.flashcard)
        with self.assertRaises(PermissionDenied):
            world_view.get_queryset()

    def test_get_queryset_method(self):
        """
        Test that the queryset_method returns words if supplied with the right
        data
        """
        request = RequestFactory()
        request.user = self.user
        world_view = WordsView()
        world_view.request = request
        world_view.kwargs = {"pk": self.flashcard.id}
        Words.objects.create(
            name="Word 1", description="Description 1", user=self.user,
            flashcard=self.flashcard)
        word = Words.objects.get(
            name="Word 1", description="Description 1", user=self.user,
            flashcard=self.flashcard)
        data = world_view.get_queryset()
        self.assertEqual(data[0], word)

    def test_ensure_access_on_flashcards(self):
        """
        Test the ensure_users_accesses_only_their_flashcards will return
        PermissionDenied Error if a flashcard does not exist, or no error if
        a flashcard exists.
        """
        with self.assertRaises(PermissionDenied):
            WordsView.ensure_users_accesses_only_their_flashcards(
                self, None, None)
        WordsView.ensure_users_accesses_only_their_flashcards(
            self, self.flashcard.id, self.user)

    def test_permissions_on_url(self):
        """
        Test that when you are not logged in to the site, that you get an
        error message
        """
        response = self.client.get("/api/v1/flashcards/{}/words/".format(1234))
        authentication_error = "Authentication credentials were not provided"
        self.assertEqual(response.status_code, 403)
        self.assertIn(authentication_error, response.content.decode("utf-8"))

    def test_get_all_words_success(self):
        """
        Test that when you are logged in to the site, you can get to view your
        words
        """
        Words.objects.create(
            name="Word 1", description="Description 1", user=self.user,
            flashcard=self.flashcard)
        word = Words.objects.get(
            name="Word 1", description="Description 1", user=self.user,
            flashcard=self.flashcard)
        self.client.force_login(self.user)
        response = self.client.get(
            "/api/v1/flashcards/{}/words/".format(self.flashcard.id))
        self.assertIn(word.name, response.content.decode("utf-8"))
        self.assertIn(word.description, response.content.decode("utf-8"))

    def test_inexistent_flashcard(self):
        """
        Test that when you visit a URL and provide a flashcard that does not
        exist that you get an error message
        """
        self.client.force_login(self.user)
        response = self.client.get(
            "/api/v1/flashcards/{}/words/".format(123456))
        self.assertEqual(response.status_code, 403)
        authentication_error = ('You do not have permission to perform'
                                ' this action.')
        self.assertIn(authentication_error, response.content.decode("utf-8"))
