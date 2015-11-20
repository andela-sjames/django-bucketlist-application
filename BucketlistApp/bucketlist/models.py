from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

# Create your models here.

class Bucketlist((models.Model)):

    '''Bucketlist Models defined here.'''

    name=models.CharField(max_length=100, blank=True)
    date_created=models.DateTimeField(auto_now_add = True)
    date_modified=models.DateTimeField(auto_now = True)
    created_by=models.CharField(max_length=100, blank=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name="buckets")
    class Meta:
        ordering = ('-date_created',)
        
class BucketlistItem(models.Model):

    '''BucketlistItem Models defined here.'''

    name=models.CharField(max_length=500, blank=True)
    date_created=models.DateTimeField(auto_now_add = True)
    date_modified=models.DateTimeField(auto_now = True)
    done = models.BooleanField()
    bucketlist=models.ForeignKey(Bucketlist, related_name="items")
    class Meta:
        ordering = ('-date_created',)
        