from django.db import models
from django.utils.translation import gettext_lazy as _


class Jargons(models.Model):
    name = models.CharField(_('jargon_name'), max_length=30, blank=True)
    description = models.TextField(_('jargon_description'))
