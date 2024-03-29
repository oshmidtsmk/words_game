#words_play

"""words_play URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace = 'accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('welcome/', views.TestPage.as_view(), name = 'test'),
    path('thanks/', views.ThanksPage.as_view(), name = 'thanks'),
    path('game/', include('game_app.urls', namespace = 'game')),
    path('oauth/', include('social_django.urls', namespace='social')),  #FB auth_backends
    #path("", include("allauth.urls")), #for Google Auth with django-allauth.
    # path('users/', views.UsersListView.as_view(), name='users_list'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
