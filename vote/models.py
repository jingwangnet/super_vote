from django.db import models

# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=50, default='')

class Vote(models.Model):
    text = models.TextField(default='')
