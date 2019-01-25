'''Urls for the app'''
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from logogram_v1.presentation.users import users
from logogram_v1.presentation.common.root import api_root

urlpatterns = [
    url(r'^$', api_root),
    url(r'^users/$', users.UsersView.as_view(), name='users'),
    url(r'^users/(?P<pk>[0-9]+)/$', users.UsersDetailView.as_view(),
        name='users-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
