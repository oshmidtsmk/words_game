#Game
from django.db import models
from django.conf import settings
import random

# Create your models here.
class Word(models.Model):
    word = models.TextField()
    description = models.TextField()
    masked_word = models.CharField(max_length=100, blank=True, null=True)

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
