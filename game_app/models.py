#Game
from django.db import models
from django.conf import settings
import random
from django.contrib.auth.models import User
from django.db.models.signals import post_save #each time when it will be saving somethign to db, we will have a hook to do something.
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number_of_attempts_to_guess = models.IntegerField(default=3)
    masked_word = models.CharField(max_length=100, blank=True, null=True)
    number_of_letter = models.IntegerField(null=True, blank=True)
    letter = models.CharField(max_length=1, blank=True, null=True)
    #guessed_word = models.ForeignKey(GuessedWords, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.user.username


class GuessedWords(models.Model):
    #word = models.CharField(max_length=100, blank=True, null=True)
    profile = models.ForeignKey(Profile,related_name="guessed_words", on_delete=models.CASCADE, blank=True, null=True)
    guessed_word = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.guessed_word



class Word(models.Model):
    #Defaul feilds for each user
    word = models.TextField()
    description = models.TextField()
    category = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.word







#Creating a user profile when the user is registered
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()


post_save.connect(create_profile, sender = User)



#
