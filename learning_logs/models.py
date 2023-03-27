from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 6th Feb 2021 - adding ForeignKey to topics to connect specific users to topics
class Topic(models.Model):  # here we inherit from model which comes with django
    '''A topic the user is learning about'''
    # here we define the class attributes
    text = models.CharField(max_length=200)  # charfield used for small text like name and city - reserve char space
    date = models.DateTimeField(auto_now_add=True)
    # ownership of topic - adding a foreign key and on-delete tells django what to do when user is deleted-cascade, delete all refs to it
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of the class'''
        return self.text


class Entry(models.Model):
    '''Entries to be added to topics - a topic could have many entries'''

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # cascade delete - deletes all entries if a topic is deleted
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''This class holds extra information to help with model management'''
        verbose_name_plural = 'entries'  # django will no longer display entrys but instead entries when referring to multiple entries

    def __str__(self):
        '''String representation of model - Display entry - but not all of it '''
        if len(self.text) < 50:
            return self.text

        return f"{self.text[:]}..."
