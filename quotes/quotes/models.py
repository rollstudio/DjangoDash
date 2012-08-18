import requests

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.contrib.sites.models import Site

from taggit.managers import TaggableManager

from allauth.socialaccount.models import SocialAccount, SocialApp

try:
    app = SocialApp.objects.get(name='Facebook')
except SocialApp.DoesNotExist:
    app = None


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Quote(models.Model):
    body = models.TextField()

    user = models.ForeignKey(User, related_name='quotes', blank=True, null=True)
    author = models.ForeignKey(Author, related_name='quotes', blank=True, null=True)

    language = models.CharField(max_length=2, choices=settings.LANGUAGES)

    source = models.CharField(max_length=200, blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('quote-detail', kwargs={'pk': self.pk})

    def get_full_url(self):
        return ''.join(['http://', Site.objects.get_current().domain, self.get_absolute_url()])


def quote_post_save(sender, instance, created, *args, **kwargs):
    if not created:
        return

    token = SocialAccount.objects.get(user=instance.user, provider='Facebook').socialtoken_set.get(app=app).token

    requests.post('https://graph.facebook.com/me/citationneeded:share', data={
        'quote': instance.get_full_url(),
        'access_token': token
    })


post_save.connect(quote_post_save, sender=Quote)
