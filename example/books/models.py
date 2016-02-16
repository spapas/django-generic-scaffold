from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
import generic_scaffold

class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    category = models.CharField(max_length=32)

    def get_absolute_url(self):
        return reverse(self.detail_url_name, args=[self.id])
