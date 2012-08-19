from django.contrib import admin

from quotes.quotes.models import Author, Quote, UserStar

admin.site.register(Author)
admin.site.register(Quote)
admin.site.register(UserStar)
