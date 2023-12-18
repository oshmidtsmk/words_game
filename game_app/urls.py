#words_game
#groups/urls.py

from django.urls import path
from . import views

app_name = 'game_app'


urlpatterns = [
    # path('descriptions/', views.DescriptionList.as_view(), name = 'game'),
    path('descriptions/<int:pk>/masking-word/', views.masking_word, name='masking-word'),
    path('descriptions/<int:pk>/new-game/', views.new_game, name='new-game'),
    path('descriptions/<int:pk>/', views.GuessingPage.as_view(), name = 'guessing_page'),
    path('user_words/<int:pk>/', views.UserWords.as_view(), name='user_profile_detail'),

]
