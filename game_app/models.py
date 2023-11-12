#Game
from django.db import models
from django.conf import settings
import random

# Create your models here.
class Word(models.Model):
    #Defaul feilds for each user
    word = models.TextField()
    description = models.TextField()
    success = models.CharField(
        max_length=100,  # Adjust the max_length as needed
        default="You have guessed it!"
        )
    failure = models.CharField(
        max_length=100,  # Adjust the max_length as needed
        default="Try again..."
        )

    call_to_action = models.CharField(
        max_length=100,  # Adjust the max_length as needed
        default="Ok make your choise now!"
        )
    you_win = models.CharField(
        max_length=100,  # Adjust the max_length as needed
        default="Congrats! You have GUESSED IT!!!!"
)

    game_over = models.CharField(
        max_length=100,  # Adjust the max_length as needed
        default="Game Over. Try again!"
)

    #Fields uniques for each user
    masked_word = models.CharField(max_length=100, blank=True, null=True)
    number_of_letter = models.IntegerField(null=True, blank=True)
    letter = models.CharField(max_length=1, blank=True, null=True)

    number_of_attempts = models.IntegerField(default=3)

    guessed = models.BooleanField(default=False)

    def __str__(self):
        return self.word

    def process_and_save(self):
        # Add your custom logic here
        self.chars = list(self.word)
        length = len(self.chars)
        # Determine the number of letters to hide (you can adjust this as needed)
        num_letters_to_hide = int(length * 0.5)  # Hiding 30% of the letters

        # Generate random indices to hide letters
        self.indices_to_hide = random.sample(range(length), num_letters_to_hide)

        # Replace the letters at the random indices with the placeholder
        for index in self.indices_to_hide:
            self.chars[index] = "*"

        # Convert the list back to a string
        self.hidden_string = "".join(self.chars)

        self.masked_word = self.hidden_string
        self.save()

    def process_reply(self):
        if self.number_of_letter and self.letter:
            if self.word[self.number_of_letter -1] == self.letter:
                temp_list = list(self.masked_word)
                temp_list[self.number_of_letter -1] = self.letter
                self.masked_word = "".join(temp_list)
                self.save()
                if self.word == self.masked_word:
                    return self.you_win
                else:
                    return self.success

            # else:
            #     if self.number_of_attempts > 0:
            #         self.number_of_attempts -= 1
            #         self.save()
            #         return self.failure
            #     else:
            #         return self.game_over


            elif self.number_of_attempts == 1:
                #self.number_of_attempts = 0
                #self.save()
                return self.game_over
            else:
                return self.failure
        else:
            if not self.number_of_letter and not self.letter:
                #self.save()
                return self.call_to_action
