from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


#from pygments import highlight

# Create your models here.
class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.now()

class Bucketlist((models.Model)):

    name=models.CharField(max_length=100, blank=True)
    public=models.BooleanField(default=False)
    date_created=models.DateTimeField(default=timezone.now)
    date_modified=AutoDateTimeField(default=timezone.now)
    created_by=models.CharField(max_length=100, blank=True)
    user=models.ForeignKey(User, related_name="buckets")
    class Meta:
        ordering = ('date_created',)

class BucketlistItems(models.Model):

    name=models.CharField(max_length=500, blank=True)
    date_created=models.DateTimeField(default=timezone.now)
    date_modified=AutoDateTimeField(default=timezone.now)
    done = models.BooleanField(default = False)
    bucketlist=models.ForeignKey(Bucketlist, related_name="items")
    class Meta:
        ordering = ('date_created',)

#Query becomes:Bucketlist.objects.filter(items__name="important")
#


