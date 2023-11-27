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

# class DescriptionList(generic.ListView):
#     model = Word
#     template_name = 'game_app/descriptions.html'  # Create an HTML template to display the list of groups
#     context_object_name = 'descriptions'

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
        # user_profile = User.objects.get(user=self.request.user)
        #
        # # Add the user profile to the context
        # context['user_profile'] = user_profile
        return context




    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = LetterForm(request.POST, instance= obj)
        if form.is_valid():
            form.save()


            if obj.process_reply() == obj.you_win:
                obj.guessed = True
                obj.save()
                return HttpResponseRedirect(reverse('game_app:you_win', kwargs={'pk': obj.pk}))

            elif obj.process_reply() == obj.failure:
                obj.number_of_attempts -= 1
                obj.save()
                return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))
            elif obj.process_reply() == obj.game_over:
                obj.number_of_attempts = 3
                obj.number_of_letter = None
                obj.letter = None
                obj.save()
                return HttpResponseRedirect(reverse('game_app:game_over', kwargs={'pk': obj.pk}))
            else:
                return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))

        else:
            # Handle form errors if needed
            return self.render_to_response(self.get_context_data(form=form))



class GameOver(generic.DetailView):
    model = Word
    template_name = 'game_app/game_over.html'
#
#
class YouWin(generic.DetailView):
    model = Word
    template_name = 'game_app/you_win.html'




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



    # obj.process_and_save(profile)  # Replace with the actual method name


    return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))
