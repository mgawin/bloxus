from django.db import models

# Create your models here.


class Game(models.Model):
    persisted_game = models.CharField(max_length=50000)
    id = models.CharField(max_length=15, primary_key=True)
