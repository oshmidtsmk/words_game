#words_game
#groups/urls.py

from django.urls import path
from . import views

app_name = 'game_app'


urlpatterns = [
    path('descriptions/', views.DescriptionList.as_view(), name = 'game'),
    path('descriptions/<int:pk>/masking-word/', views.masking_word, name='masking-word'),
    path('descriptions/<int:pk>/', views.GuessingPage.as_view(), name = 'guessing_page'),
    # path('descriptions/game_over/<int:pk>/', views.GameOver.as_view(), name = 'game_over'),
    path('descriptions/you_win_over/<int:pk>/', views.YouWin.as_view(), name = 'you_win'),
]
