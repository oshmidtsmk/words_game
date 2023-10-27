from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import generic
from .models import Word
from .forms import LetterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .game_play import Puzzle

# Create your views here.

class DescriptionList(generic.ListView):
    model = Word
    template_name = 'game_app/descriptions.html'  # Create an HTML template to display the list of groups
    context_object_name = 'descriptions'


class GuessingPage(generic.DetailView):
    model = Word
    template_name = 'game_app/guessing_page.html'  # Create an HTML template to display the group details
    context_object_name = 'puzzle'

    # def post(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.process_and_save()
    #     return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': instance.pk}))

def masking_word(request, pk):
    obj = Word.objects.get(pk=pk)

    # Call the method on the object
    obj.process_and_save()  # Replace with the actual method name

    # Redirect to the DetailView for the selected item
    #return redirect('game_app:guessing_page', pk=pk)
    return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))
