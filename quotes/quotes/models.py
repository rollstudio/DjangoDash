from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Quote(models.Model):
    body = models.TextField()

    user = models.ForeignKey(User, related_name='quotes', blank=True, null=True)
    author = models.ForeignKey(Author, related_name='quotes')

    language = models.CharField(max_length=2, choices=settings.LANGUAGES)

    tags = TaggableManager()
