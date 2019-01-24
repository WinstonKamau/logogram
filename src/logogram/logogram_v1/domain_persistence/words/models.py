from django.db import models
from django.utils.translation import gettext_lazy as _
from logogram_v1.domain_persistence.flashcards.models import FlashCards
from logogram_v1.domain_persistence.users.models import Users
from django.utils import timezone


class Words(models.Model):
    name = models.CharField(_('word_name'), max_length=30, blank=True)
    description = models.TextField(_('word_description'))
    creation_date = models.DateTimeField(_('date_created'),
                                         default=timezone.now)
    modification_date = models.DateTimeField(_('date_modified'),
                                             auto_now_add=True)
    flash_card = models.ForeignKey(FlashCards, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
