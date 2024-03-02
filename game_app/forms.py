from django import forms
from .models import Profile
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class GuessForm(forms.Form):
    def __init__(self, masked_word, *args, **kwargs):
        super(GuessForm, self).__init__(*args, **kwargs)

        for i, letter in enumerate(masked_word):
            field_name = f'guessed_{i + 1}'  # Unique field name for each masked letter
            #initial_value = guessed_letters.get(field_name, '')

            if letter == '*':
                self.fields[field_name] = forms.CharField(max_length=1, required=False,
                widget=forms.TextInput(attrs={'style': 'width: 40px; height:40px; text-align: center;'})
                )


            else:
                self.fields[field_name] = forms.CharField(
                    max_length=1,
                    required=False,
                    widget=forms.TextInput(attrs={'readonly': 'readonly', 'disabled': 'disabled', 'placeholder':letter, 'style': 'width: 40px; height:40px; text-align: center;'})
                )


class UserEditForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
