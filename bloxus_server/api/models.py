from django.db import models

# Create your models here.


class Game(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    persisted_game = models.CharField(max_length=50000)
    robot_game = models.BooleanField(default=False)


class WaitingGame(models.Model):
    gid = models.CharField(max_length=15)
    id = models.AutoField(primary_key=True)
