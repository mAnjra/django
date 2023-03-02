from django.core.management.base import BaseCommand
from django.db import models


# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    my_boolean_field = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title