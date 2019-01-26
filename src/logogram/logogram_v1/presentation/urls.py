'''Urls for the app'''
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from logogram_v1.presentation.users import users
from logogram_v1.presentation.common.root import api_root
from logogram_v1.presentation.flashcards import flashcards
from django.http import request

urlpatterns = [
    url(r'^$', api_root),
    url(r'^users/$', users.UsersView.as_view(), name='users'),
    url(r'^users/(?P<pk>[0-9]+)/$', users.UsersDetailView.as_view(),
        name='users-detail'),
    url(r'^flashcards/$', flashcards.FlashCardsView.as_view(),
        name='flashcards'),
    url(r'^flashcards/(?P<pk>[0-9]+)/$',
        flashcards.FlashCardsDetailView.as_view(), name='flashcards-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
