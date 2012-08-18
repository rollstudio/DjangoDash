from django import forms

from .models import Quote


class QuoteForm(forms.ModelForm):
    author = forms.CharField()

    class Meta:
        model = Quote
        exclude = ('user', 'metadata', 'author')
