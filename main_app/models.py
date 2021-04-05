from django.db import models
from django.urls import reverse
from datetime import date
# thank you Django for this user :-)
from django.contrib.auth.models import User
# Create your models here.

class JobsCat(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)
    def __str__(self):
        return self.name

class Jobs(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    comp = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)
    def __str__(self):
        return self.name

class Saved(models.Model):
    category = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    comp = models.CharField(max_length=100, default='')
    link = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


PRI = (
    ('H', 'High'),
    ('M', 'Medium'),
    ('L', 'Low')
)

class Note(models.Model):
    date = models.DateField('Due Date')
    priority = models.CharField(
        max_length=1,
        choices = PRI,
        default = PRI[0][0]
    )
    content = models.CharField(max_length=1000, default='')
    done = models.BooleanField(default=False)

    saved = models.ForeignKey(Saved, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_priority_display()} on {self.date}"