from logogram_v1.domain_persistence.flashcards.models import FlashCards
from logogram_v1.application.flashcards.flashcards import (
    FlashCardsSerializer, FlashCardsDetailSerializer)
from rest_framework import generics
from rest_framework.authentication import (SessionAuthentication, 
    BasicAuthentication)
from rest_framework.permissions import IsAuthenticated


class FlashCardsView(generics.ListCreateAPIView):
    """
    List all flashcards for a user
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = FlashCardsSerializer

    def get_queryset(self):
        '''
        This view should return a list of all the flashcards for the currently
        authenticated user.
        '''
        user = self.request.user
        return FlashCards.objects.filter(user=user)


class FlashCardsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a flashcard for a user
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = FlashCardsDetailSerializer

    def get_queryset(self):
        '''
        This view should return one of the flashcards for the currently
        authenticated user.
        '''
        user = self.request.user
        return FlashCards.objects.filter(user=user, id=self.kwargs.get("pk"))
