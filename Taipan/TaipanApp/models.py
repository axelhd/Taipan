from django.db import models

# Create your models here.


class Command(models.Model):
    completed = models.BooleanField(default=False)
    #Create text field for command
    command = models.TextField(default='')
    target = models.IntegerField(default=0)
    output = models.TextField(default='')
