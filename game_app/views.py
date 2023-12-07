from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views import generic
from .models import Word, Profile
from django.contrib.auth.models import User
from .forms import LetterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .game_play import Puzzle
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import Http404
import random


# Create your views here.

class UserWords(generic.DetailView):
    """
    Words to guess for the current user
    """
    model = Profile
    template_name = 'game_app/user_words.html'  # Create an HTML template to display the list of groups
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['words'] = Word.objects.all()
        return context



class GuessingPage(LoginRequiredMixin, generic.DetailView):
    model = Word
    template_name = 'game_app/guessing_page.html'  # Create an HTML template to display the group details
    context_object_name = 'puzzle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LetterForm(instance=self.object)
         # Retrieve 'your_string' from the query parameters
        condition_string = self.request.GET.get('condition_string', None)

        # Add 'your_string' to the context
        context['condition_string'] = condition_string
        return context

    def post(self, request, *args, **kwargs):
        #obj = self.get_object() ##
        word_obj = self.get_object()
        profile_obj = request.user.profile
        form = LetterForm(request.POST, instance= profile_obj)
        if form.is_valid():
            form.save()

            if profile_obj.number_of_letter and profile_obj.letter:
                if word_obj.word[profile_obj.number_of_letter -1] == profile_obj.letter:
                    temp_list = list(profile_obj.masked_word)
                    temp_list[profile_obj.number_of_letter -1] = profile_obj.letter
                    profile_obj.masked_word = "".join(temp_list)
                    profile_obj.save()
                    if word_obj.word == profile_obj.masked_word:
                        #return HttpResponseRedirect(reverse('game_app:you_win', kwargs={'pk': word_obj.pk}))
                        return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': word_obj.pk}))
                    else:
                        condition_string = "You have quessed it!"
                        redirect_url = reverse('game_app:guessing_page', kwargs={'pk': word_obj.pk})
                        return HttpResponseRedirect(f"{redirect_url}?condition_string={condition_string}")
                        #return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': word_obj.pk}))
                else:
                    profile_obj.number_of_attempts_to_guess -=1
                    profile_obj.save()
                    condition_string = "No:("
                    redirect_url = reverse('game_app:guessing_page', kwargs={'pk': word_obj.pk})
                    return HttpResponseRedirect(f"{redirect_url}?condition_string={condition_string}")
                    #return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': word_obj.pk}))
            else:
                condition_string = "Plase make your choice"
                redirect_url = reverse('game_app:guessing_page', kwargs={'pk': word_obj.pk})
                return HttpResponseRedirect(f"{redirect_url}?condition_string={condition_string}")
                return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': word_obj.pk}))
        else:
            return self.render_to_response(self.get_context_data(form=form))



class GameOver(generic.DetailView):
    model = Word
    template_name = 'game_app/game_over.html'
#
#
class YouWin(LoginRequiredMixin, generic.DetailView):
    model = Word
    template_name = 'game_app/you_win.html'


def new_game(request, pk):
    word_obj = Word.objects.get(pk=pk)
    profile_obj = request.user.profile
    profile_obj.number_of_attempts_to_guess = 3
    profile_obj.number_of_letter = None
    profile_obj.letter = None
    profile_obj.save()
    #return HttpResponseRedirect(reverse('game_app:user_words', kwargs={'pk': word_obj.pk}))
    return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': word_obj.pk}))



def masking_word(request, pk):
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

    # Convert the list back to a string
    obj.hidden_string = "".join(obj.chars)

    user.profile.masked_word = obj.hidden_string
    user.profile.save()


    return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))
