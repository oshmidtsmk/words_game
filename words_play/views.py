#words_play

#from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views import generic

class TestPage(TemplateView):
    template_name = 'welcome.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = "index.html"

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated():
    #         return HttpResponseRedirect(reverse("test"))
    #     return super().get(request, *args, **kwargs)

# class UsersListView(generic.ListView):
#     model = User
#     template_name = 'users_list.html'
#     context_object_name = 'people'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         context['user'] = user
#         return context
