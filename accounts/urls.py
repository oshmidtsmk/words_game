#words_play

from django.urls import path, include
from django.contrib.auth import views as auth_views # is automatically providing build in login/logout views.
from accounts import views


app_name = 'accounts'


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),# it goes to homepahe
    path('signup/', views.SignUp.as_view(), name = 'signup'),
    #path('oauth/', include('social_django.urls', namespace='social')),  #FB
    #for password resetting
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),

]
