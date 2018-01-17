from __future__ import unicode_literals

try:
    from django.core.urlresolvers import reverse
except ModuleNotFoundError:
    from django.urls import reverse

from django.db import models
import generic_scaffold

class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    category = models.CharField(max_length=32)

    def get_absolute_url(self):
        return reverse(self.detail_url_name, args=[self.id])

    def __str__(self):
        return '{0} {1} {2}'.format(self.title, self.author, self.category)
