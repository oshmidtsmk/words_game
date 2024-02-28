#words_game
#groups/urls.py

from django.urls import path
from . import views

app_name = 'game_app'


urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<str:category>/<int:pk>/masking-word/', views.masking_word, name='masking-word'),
    path('categories/<str:category>/', views.WordListView.as_view(), name='word_list'),
    path('categories/<str:category>/<int:pk>/', views.GuessingPage.as_view(), name='guessing_page'),
    path('categories/<str:category>/<int:pk>/new-game/', views.new_game, name='new-game'),
    path('players/', views.PlayersListView.as_view(), name='players_list'),
    path('players/<int:pk>/', views.PlayerView.as_view(), name='player_page'),
    path('players/<int:pk>/edit/', views.EditUserView.as_view(), name='edit_user'),

]
