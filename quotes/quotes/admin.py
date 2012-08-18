from django.contrib import admin

from quotes.quotes.models import Author, Quote

admin.site.register(Author)
admin.site.register(Quote)
