from logogram_v1.domain_persistence.words.models import Words
from logogram_v1.application.words.words import (
    WordsSerializer, WordsDetailSerializer)
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from logogram_v1.domain_persistence.flashcards.models import FlashCards
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated


class WordsView(generics.ListCreateAPIView):
    """
    List all words for a flashcard
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = WordsSerializer

    def get_queryset(self):
        """
        This view should return the words of a particular flashcard.
        """
        user = self.request.user
        self.ensure_users_accesses_only_their_flashcards(
            self.kwargs["pk"], user)
        return Words.objects.filter(flashcard=self.kwargs["pk"], user=user)

    def ensure_users_accesses_only_their_flashcards(self, flashcard_id, user):
        flashcard = FlashCards.objects.filter(
            id=flashcard_id, user=user).first()
        if not flashcard:
            raise PermissionDenied()


class WordsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a word
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = WordsDetailSerializer
    queryset = Words.objects.all()

    def get_queryset(self):
        """
        This view should return one of the words for a flashcard of the
        currently authenticated user.
        """
        user = self.request.user
        WordsView().ensure_users_accesses_only_their_flashcards(
            self.kwargs["flashcard_pk"], user)
        return Words.objects.filter(flashcard=self.kwargs["flashcard_pk"],
                                    user=user, id=self.kwargs["pk"])
