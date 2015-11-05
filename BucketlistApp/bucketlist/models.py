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
    private=models.BooleanField(default=True)
    date_created=models.DateField(default=timezone.now)
    date_modified=AutoDateTimeField(default=timezone.now)
    created_by=models.CharField(max_length=100, blank=True)
    user=models.ForeignKey(User, related_name="bucket", related_query_name="buckets")

class BucketlistItems(models.Model):

    name=models.CharField(max_length=500, blank=True)
    date_created=models.DateField(default=timezone.now)
    date_modified=AutoDateTimeField(default=timezone.now)
    done = models.BooleanField(default = False)
    bucketlist=models.ForeignKey(Bucketlist, related_name="item", related_query_name="items")

#Query becomes:Bucketlist.objects.filter(item__name="important")



