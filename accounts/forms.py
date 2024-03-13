#words_play

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _ #for translation of the form.
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


        # Override default password validation messages
        self.fields["username"].help_text = _(
        "Обов'язково. 150 символів або менше. Тільки літери, цифри та символи @/./+/-/_."
        )
        self.fields["password1"].help_text = _(
            "Ваш пароль повинен містити принаймні 8 символів,<br> "
            "не може бути надто схожим на вашу іншу особисту інформацію,<br> "
            "і не може бути занадто популярним паролем. <br>"
            )
        self.fields["password2"].help_text = _("Введіть той самий пароль, що й раніше, для підтвердження.")
