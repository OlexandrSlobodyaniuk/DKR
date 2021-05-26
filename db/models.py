from django.db import models

class Match(models.Model):
    team_one = models.CharField(max_length=255)
    team_two = models.CharField(max_length=255)
    date = models.DateTimeField()
    town = models.CharField(max_length=255)


