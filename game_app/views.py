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

    # def get(self, request, *args, **kwargs):
    #     # Retrieve the instance of the model
    #     self.object = self.get_object()
    #
    #     # Add your condition here
    #     if self.object.number_of_attempts < 0:  # Replace with your condition
    #         # Redirect to another page
    #         #return redirect('game_app:game_over')  # Replace with the name of the view to redirect to
    #         return HttpResponseRedirect(reverse('game_app:game_over', kwargs={'pk': self.object.pk}))
    #
    #     # If the condition is not met, continue with the default behavior
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = LetterForm(request.POST, instance= obj)
        if form.is_valid():
            form.save()
            #return redirect('game_app:guessing_page', pk=obj.pk)
            if obj.number_of_attempts < 0:
                return HttpResponseRedirect(reverse('game_app:game_over', kwargs={'pk': obj.pk}))
            else:
                return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))
        else:
            # Handle form errors if needed
            return self.render_to_response(self.get_context_data(form=form))

class GameOver(generic.DetailView):
    model = Word
    template_name = 'game_app/game_over.html'


# class YouWin(generic.DetailView):
#     model = Word
#     template_name = 'game_app/you_win.html'




def masking_word(request, pk):
    obj = Word.objects.get(pk=pk)

    # Call the method on the object
    obj.process_and_save()  # Replace with the actual method name

    # Redirect to the DetailView for the selected item
    #return redirect('game_app:guessing_page', pk=pk)
    return HttpResponseRedirect(reverse('game_app:guessing_page', kwargs={'pk': obj.pk}))
