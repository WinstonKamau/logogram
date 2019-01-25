'''Urls for the app'''
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from logogram_v1.presentation.users import users
from logogram_v1.presentation.common.root import api_root

urlpatterns = [
    url(r'^$', api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)
