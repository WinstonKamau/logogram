from django.db import models
from django.utils.translation import gettext_lazy as _
from logogram_v1.domain_persistence.jargons.models import Jargons
from logogram_v1.domain_persistence.users.models import Users
from django.utils import timezone


class FlashCards(models.Model):
    name = models.CharField(_('flash_card_name'), max_length=30, blank=True)
    description = models.TextField(_('flash_card_description'))
    creation_date = models.DateTimeField(_('date_created'), default=timezone.now)
    modification_date = models.DateTimeField(_('date_modified'), auto_now_add=True)
    privacy = models.BooleanField(_('privacy status'), default=True, help_text=_(
        'Designates whether the flashcards are private or public.'),)
    jargon = models.ForeignKey(Jargons, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
