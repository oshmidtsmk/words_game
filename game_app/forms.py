from django import forms
from .models import Profile

class LetterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['number_of_letter', 'letter']
