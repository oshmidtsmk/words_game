from django.shortcuts import render
from django.shortcuts import redirect
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LetterForm(instance=self.object)
        return context





    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = LetterForm(request.POST, instance= obj)
        if form.is_valid():
            form.save()
            print(obj.process_reply())


            if obj.process_reply() == obj.you_win:
                return HttpResponseRedirect(reverse('game_app:you_win', kwargs={'pk': obj.pk}))

            elif obj.process_reply() == obj.failure:
                obj.number_of_attempts -= 1
                obj.save()
                return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))
            elif obj.process_reply() == obj.game_over:
                return HttpResponseRedirect(reverse('game_app:game_over', kwargs={'pk': obj.pk}))

            #if obj.process_reply() == obj.failure:
            else:
                return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))
            # return self.win_lose()
        else:
            # Handle form errors if needed
            return self.render_to_response(self.get_context_data(form=form))

    # def win_lose(self):
    #     obj = self.get_object()
    #     if obj.masked_word == obj.word:
    #         print(obj.masked_word)
    #         return HttpResponseRedirect(reverse('game_app:you_win', kwargs={'pk': obj.pk}))
    #     else:
    #         return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))



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

    # Call the method on the object
    obj.process_and_save()  # Replace with the actual method name

    # Redirect to the DetailView for the selected item
    #return redirect('game_app:guessing_page', pk=pk)
    return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))
