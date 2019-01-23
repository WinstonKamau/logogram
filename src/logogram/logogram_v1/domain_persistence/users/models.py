from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, error_messages={
            'unique': _("The email address you entered has already been registered.",), },
                        max_length=255)
    first_name = models.CharField(_('first_name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # Require the email and password only
    REQUIRED_FIELDS = []
