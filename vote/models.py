from django.db import models
from django.urls import reverse

# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=50, default='')

    def get_absolute_url(self):
        return reverse('view_question', kwargs={'pk':self.pk})

class Vote(models.Model):
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE
    )
    text = models.TextField(default='')
