from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views import generic
from .models import Word, Profile, GuessedWords
from django.contrib.auth.models import User
#from .forms import LetterForm
from .forms import GuessForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import Http404
import random


# Create your views here.

class CategoryListView(generic.ListView):
    model = Word
    template_name = 'game_app/category_list.html'
    context_object_name = 'categories'
    queryset = Word.objects.values('category').distinct() # to show only one the same category without duplicates.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context

class WordListView(generic.ListView):
    model = Word
    template_name = 'game_app/word_list.html'
    context_object_name = 'words'

    def get_queryset(self):
        return Word.objects.filter(category=self.kwargs['category']) #this category is passed from html by click.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['category'] = self.kwargs['category']

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

        user_profile = self.request.user.profile
        masked_word = user_profile.masked_word

        condition_string = self.request.GET.get('condition_string', None)
        context['form'] = GuessForm(masked_word)
        context['masked_word'] = masked_word
        context['user_profile'] = self.request.user.profile
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
                if guessed_letter == original_letter:
                    masked_word_list[index] = guessed_letter
                    condition_strings.append("All is right")
                    guessed_letters.append(guessed_letter)

                elif guessed_letter != original_letter and guessed_letter != '':
                    user_profile.number_of_attempts_to_guess -= 1
                    condition_strings.append("No")
                    missed_letters.append(guessed_letter)


    # Update user_profile outside the loop
            user_profile.masked_word = ''.join(masked_word_list)
            user_profile.save()
            if word_obj.word == user_profile.masked_word:
                        guessed_word_instance = GuessedWords.objects.create(
                            profile = user_profile,
                            guessed_word = word_obj.word
                        )

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




        #     return redirect('success_page')  # Redirect to a success page or any other appropriate view
        #
        # return self.render_to_response(self.get_context_data(form=form))



def new_game(request,category, pk):
    word_obj = Word.objects.get(pk=pk)
    profile_obj = request.user.profile
    profile_obj.number_of_attempts_to_guess = 3
    profile_obj.number_of_letter = None
    profile_obj.letter = None
    profile_obj.save()

    #return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': word_obj.pk}))
    return HttpResponseRedirect(reverse('game_app:guessing_page', args=[category, pk]))




def masking_word(request,category, pk):
    obj = Word.objects.get(pk=pk)
    user = request.user

    # Add your custom logic here
    obj.chars = list(obj.word)
    length = len(obj.chars)
    # Determine the number of letters to hide (you can adjust this as needed)
    num_letters_to_hide = int(length * 0.5)  # Hiding 30% of the letters

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
    #obj.hidden_string = "".join(obj.chars)
    obj.hidden_string = "".join(masked_list)


    user.profile.masked_word = obj.hidden_string
    user.profile.save()

    return HttpResponseRedirect(reverse('game_app:guessing_page', args=[category, pk]))# category and pk args are passed from html
