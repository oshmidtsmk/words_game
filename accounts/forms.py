#words_play

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# from django.utils.translation import gettext_lazy as _ #for translation of the form.
# from django.contrib.auth.forms import AuthenticationForm
# from django import forms


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Ім'я'"
        self.fields["email"].label = "Пошта"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Підтвердженя паролю"
