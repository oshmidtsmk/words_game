from django.views import generic
from .models import Word, Profile, GuessedWords
from django.contrib.auth.models import User
from django.db import models #is used for rating of players by bumber of guessed word in the players view.
from .forms import GuessForm, UserEditForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import random


# Create your views here.

class CategoryListView(generic.ListView):
    model = Word
    template_name = 'game_app/category_list.html'
    context_object_name = 'categories'
    queryset = Word.objects.values('category').distinct() # to show only one the same category without duplicates.

    # def get_queryset(self):
    #     Word.objects.values('category').distinct() # to show only one the same category without duplicates.


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class PlayersListView(generic.ListView):
    model = User
    template_name = 'game_app/players_list.html'
    context_object_name = 'players'

    def get_queryset(self):
        #showind descending number of guessed words
        return User.objects.annotate(num_guessed_words=models.F('profile__number_of_guessed_words')).order_by('-num_guessed_words')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context['user'] = user
        return context

class PlayerView(generic.DetailView):
    model = User
    template_name = 'game_app/player_page.html'  # Create an HTML template to display the group details
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = context[self.context_object_name]
        guessed_words = []
        for item in player.profile.guessed_words.all():
            if item.guessed_category:
                item = (str(item.guessed_word),str(item.guessed_category))
            else:
                item = (str(item.guessed_word), "без категорії")
            guessed_words.append(item)

        context['guessed_words'] = guessed_words
        statistics = {}
        for item in guessed_words:
            second_item = item[1]
            statistics[second_item] = statistics.get(second_item, 0) + 1
        context['statistics'] = statistics
        user = self.request.user
        context['user'] = user

        return context

class EditUserView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'game_app/edit_user.html'
    form_class = UserEditForm

    
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        # Get the pk of the current user
        pk = self.request.user.pk
        return reverse_lazy('game_app:player_page', kwargs={'pk': pk})




class WordListView(generic.ListView):
    model = Word
    template_name = 'game_app/word_list.html'
    context_object_name = 'words'

    def get_queryset(self):
        category = self.kwargs.get('category')  # Use get() to handle the case when 'category' is absent
        if category:
            return Word.objects.filter(category=category)
        else:
            return Word.objects.all()  # You can modify this to return an empty queryset or handle it as needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['category'] = self.kwargs.get('category', '')  # Provide a default value if 'category' is absent
        #here I am just making a list out of the queriset to work with it in html of words_list
        guessed_words = []
        for item in user.profile.guessed_words.all():
            item = str(item)
            guessed_words.append(item)

        context['guessed_words'] = guessed_words

        return context

class GuessingPage(LoginRequiredMixin, generic.DetailView):
    model = Word
    template_name = 'game_app/guessing_page.html'  # Create an HTML template to display the group details
    context_object_name = 'word'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        masked_word = self.request.user.profile.masked_word
        condition_string = self.request.GET.get('condition_string', None)

        context['user'] = self.request.user
        context['form'] = GuessForm(masked_word)
        context['condition_string'] = condition_string

        return context

    def post(self, request,category, pk, *args, **kwargs):
        word_obj = self.get_object()
        user_profile = request.user.profile
        masked_word_list = list(user_profile.masked_word)

        form = GuessForm(user_profile.masked_word, request.POST)


        if form.is_valid():

            condition_strings = []  # List to store condition stringsґ
            guessed_letters = []
            missed_letters = []

            for index, (guessed_letter, original_letter) in enumerate(zip(form.cleaned_data.values(), word_obj.word)):

                if guessed_letter.lower() == original_letter.lower():
                    masked_word_list[index] = guessed_letter
                    condition_strings.append("All is right")
                    guessed_letters.append(guessed_letter.upper())

                elif guessed_letter.lower() != original_letter.lower() and guessed_letter != '':
                    user_profile.number_of_attempts_to_guess -= 1
                    condition_strings.append("No")
                    missed_letters.append(guessed_letter.upper())



    # Update user_profile outside the loop
            user_profile.masked_word = ''.join(masked_word_list)
            user_profile.save()
            if word_obj.word == user_profile.masked_word:
                        guessed_word_instance = GuessedWords.objects.create(
                            profile = user_profile,
                            guessed_word = word_obj.word,
                            guessed_category = word_obj.category
                        )
                        user_profile.number_of_guessed_words +=1
                        user_profile.save()

            guessed_letters = ", ".join(guessed_letters)
            missed_letters = ", ".join(missed_letters)

            # Decide the redirect URL based on the accumulated condition strings
            if "All is right" in condition_strings and "No" in condition_strings:
                condition_string = f"Ці літери правильні: {guessed_letters}, а ось ці, нажаль,ні: {missed_letters}. За кожну невірну літеру знято 1 бал "
            elif "All is right" in condition_strings:
                condition_string = f"Всі обрані літери правильні! {guessed_letters}"
            elif "No" in condition_strings:
                condition_string = f"Нажаль усі введені літери невірні: {missed_letters}. За кожну невірну літеру знято 1 бал "
            else:
                condition_string = "Зроби свій вибір, щеня!!!"

    # Redirect with the final condition string
            redirect_url = reverse('game_app:guessing_page', args=[category, pk])
            return HttpResponseRedirect(f"{redirect_url}?condition_string={condition_string}")

# Redirect if the form is not valid or after the loop

        return HttpResponseRedirect(reverse('game_app:guessing_page', args=[category, pk]))


def new_game(request,category, pk):
    word_obj = Word.objects.get(pk=pk)
    profile_obj = request.user.profile
    profile_obj.number_of_attempts_to_guess = 3
    profile_obj.number_of_letter = None
    profile_obj.letter = None
    profile_obj.save()


    return HttpResponseRedirect(reverse('game_app:guessing_page', args=[category, pk]))




def masking_word(request,category, pk):
    obj = Word.objects.get(pk=pk)
    user = request.user

    # Add your custom logic here
    obj.chars = list(obj.word)
    length = len(obj.chars)
    # Determine the number of letters to hide (you can adjust this as needed)
    num_letters_to_hide = int(length * 0.5)  # Hiding 50% of the letters

    # Generate random indices to hide letters
    obj.indices_to_hide = random.sample(range(length), num_letters_to_hide)

    # Replace the letters at the random indices with the placeholder
    for index in obj.indices_to_hide:
        obj.chars[index] = "*"


    masked_list = []

    for letter,masked in zip(obj.word,obj.chars):
        if letter == " ":
            masked_letter = " "
            masked_list.append(masked_letter)
        elif letter == "-":
            masked_letter = "-"
            masked_list.append(masked_letter)
        else:
            masked_letter = masked
            masked_list.append(masked_letter)

    # Convert the list back to a string
    obj.hidden_string = "".join(masked_list)

    user.profile.masked_word = obj.hidden_string
    user.profile.save()

    return HttpResponseRedirect(reverse('game_app:guessing_page', args=[category, pk]))# category and pk args are passed from html
