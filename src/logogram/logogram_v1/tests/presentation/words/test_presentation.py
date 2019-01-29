"""Test presentation of the Words entity """
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.presentation.words.words import WordsView, WordsDetailView
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
        response = self.client.get(
            "/api/v1/flashcards/{}/words/".format(1234))
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


class WordsDetailViewPresentation(BaseTestCase):

    def setUp(self):
        Users.objects.create(
            email="buttercup@gmail.com", first_name="Butter", last_name="Cup")
        self.user = Users.objects.get(email="buttercup@gmail.com")
        self.request = RequestFactory()
        self.request.user = self.user
        FlashCards.objects.create(
            name="Flashcard 1", description="Description1", user=self.user)
        self.flashcard = FlashCards.objects.get(name="Flashcard 1")
        Words.objects.create(name="Word 1", description="Description Word 1",
                             user=self.user, flashcard=self.flashcard)
        self.word = Words.objects.get(name="Word 1")
        super(WordsDetailViewPresentation, self).setUp()

    def test_retrieve_word(self):
        """
        Test that a word can be retrieved
        """
        self.client.force_login(self.user)
        response = self.client.get(
            "/api/v1/flashcards/{}/words/{}/".format(
                self.flashcard.id, self.word.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.word.name, response.content.decode("utf-8"))
        self.assertIn(self.word.description, response.content.decode("utf-8"))

    def test_permissions_required(self):
        """
        Test that permissions are required to be able to view words on a
        flashcard. A non logged in user cannot access the words URL.
        """
        response = self.client.get(
            "/api/v1/flashcards/{}/words/{}/".format(
                self.flashcard.id, self.word.id))
        self.assertEqual(response.status_code, 403)

    def test_retrieve_own_word(self):
        """
        Test that you can only retrieve your own word.
        """
        Users.objects.create(
            email="spongebog@gmail.com", first_name="Sponge", last_name="Bob")
        self.user = Users.objects.get(email="spongebog@gmail.com")
        self.client.force_login(self.user)
        response = self.client.get(
            "/api/v1/flashcards/{}/words/{}/".format(
                self.flashcard.id, self.word.id))
        self.assertEqual(response.status_code, 403)
        authentication_error = ('You do not have permission to perform'
                                ' this action.')
        self.assertIn(authentication_error, response.content.decode("utf-8"))

    def test_word_not_found(self):
        """
        Test that when you access your own flashcard and for a word with the
        wrong word id you get a NOT Found error
        """
        Users.objects.create(
            email="spongebog@gmail.com", first_name="Sponge", last_name="Bob")
        self.user = Users.objects.get(email="spongebog@gmail.com")
        self.client.force_login(self.user)
        FlashCards.objects.create(
            name="Flashcard 3", description="Description3", user=self.user)
        bob_flashcard = FlashCards.objects.get(name="Flashcard 3")
        response = self.client.get(
            "/api/v1/flashcards/{}/words/{}/".format(
                bob_flashcard.id, self.word.id))
        self.assertEqual(response.status_code, 404)
        not_found_error = ('Not found.')
        self.assertIn(not_found_error, response.content.decode("utf-8"))

    def test_get_queryset_method(self):
        """
        Test that the queryset_method returns words if supplied with the right
        data
        """
        request = RequestFactory()
        request.user = self.user
        world_detail_view = WordsDetailView()
        world_detail_view.request = request
        Words.objects.create(
            name="Word 2", description="Description 2", user=self.user,
            flashcard=self.flashcard)
        word = Words.objects.get(
            name="Word 2", description="Description 2", user=self.user,
            flashcard=self.flashcard)
        world_detail_view.kwargs = {
            "flashcard_pk": self.flashcard.id, "pk": word.pk}
        data = world_detail_view.get_queryset()
        self.assertEqual(data[0], word)

    def test_word_deletion(self):
        """
        Test that when you delete a word it no longer exists in the database
        """
        self.assertIsNotNone(Words.objects.filter(id=self.word.id).first())
        self.client.force_login(self.user)
        self.client.delete("/api/v1/flashcards/{}/words/{}/".format(
            self.flashcard.id, self.word.id))
        self.assertIsNone(Words.objects.filter(id=self.word.id).first())

    def test_word_edition(self):
        """
        Test that when you edit a word, its attributes change
        """
        self.assertEqual(self.word.name, "Word 1")
        self.assertEqual(self.word.description, "Description Word 1")
        data = {"name": "Edited Name", "description": "Edited Description"}
        self.client.force_login(self.user)
        self.client.put("/api/v1/flashcards/{}/words/{}/".format(
            self.flashcard.id, self.word.id), data,
            content_type='application/json')
        word = Words.objects.get(id=self.word.id)
        self.assertEqual(word.name, data["name"])
        self.assertEqual(word.description, data["description"])
