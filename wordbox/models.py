# models.py

from django.db import models
from django.contrib.auth.models import User

# models.py
class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    meaning = models.TextField()
    saved_at = models.DateTimeField(auto_now_add=True, null=True)  # Make it nullable
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.word
