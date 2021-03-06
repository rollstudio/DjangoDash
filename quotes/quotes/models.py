from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.sites.models import Site

from taggit.managers import TaggableManager

import facebook

from allauth.socialaccount.models import SocialAccount, SocialApp


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Quote(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    excerpt = models.CharField(max_length=255, blank=True, editable=False)
    body = models.TextField()

    user = models.ForeignKey(User, related_name='quotes', blank=True, null=True)
    author = models.ForeignKey(Author, related_name='quotes', blank=True, null=True)

    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                default="en")

    source = models.CharField(max_length=200, blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)

    published_on = models.DateTimeField(auto_now_add=True)

    star_count = models.IntegerField(default=0)

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('quote-detail', kwargs={'pk': self.pk})

    def get_full_url(self):
        return ''.join(['http://', Site.objects.get_current().domain, self.get_absolute_url()])

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.body[:50]

    def get_excerpt(self):
        return self.excerpt if self.excerpt else self.body[:255]


class UserStar(models.Model):

    class Meta:
        unique_together = (('user', 'quote'),)

    user = models.ForeignKey(User, related_name='stars')
    quote = models.ForeignKey(Quote, related_name='starts')

    def __unicode__(self):
        return '%s <3 %s' % (self.user.username, self.quote)


def quote_post_save(sender, instance, created, *args, **kwargs):
    if not created:
        return

    try:
        app = SocialApp.objects.get(name='Facebook')
    except SocialApp.DoesNotExist:
        app = None

    if app == None:
        return

    try:
        token = SocialAccount.objects.get(user=instance.user, provider='facebook').socialtoken_set.get(app=app).token

        graph = facebook.GraphAPI(token)
        graph.put_object("me", "citationneeded:share", quote=instance.get_full_url())

    except models.ObjectDoesNotExist:
        pass

#post_save.connect(quote_post_save, sender=Quote)

def quote_set_excerpt(sender, instance, raw, using, **kwargs):
    chunks = instance.body.split('---', 1)
    if len(chunks) > 1:
        instance.excerpt = chunks[0][:255]
        instance.body = ''.join(chunks)

pre_save.connect(quote_set_excerpt, sender=Quote)


def star_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.quote.star_count += 1
        instance.quote.save()

post_save.connect(star_post_save, sender=UserStar)

def star_post_delete(sender, instance, using, **kwargs):
    if instance.quote.star_count > 0:
        instance.quote.star_count -= 1
    instance.quote.save()

post_delete.connect(star_post_delete, sender=UserStar)
