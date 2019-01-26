from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'), unique=True, error_messages={
            'unique': _("The email address you entered has already been "
                        "registered.",), },
        max_length=255)
    first_name = models.CharField(_('first_name'), max_length=30)
    last_name = models.CharField(_('last_name'), max_length=30)
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'),)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # Require the email and password only
    REQUIRED_FIELDS = []
