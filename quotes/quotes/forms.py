from django import forms

from .models import Quote


class QuoteForm(forms.ModelForm):
    author_field = forms.CharField(label='Author', required=False)

    class Meta:
        model = Quote
        exclude = ('user', 'metadata', 'author')

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        for label, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.help_text
            field.help_text = None
