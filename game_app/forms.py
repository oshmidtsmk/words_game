from django import forms
from .models import Word

class LetterForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['number_of_letter', 'letter']
