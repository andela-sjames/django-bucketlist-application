'''Script registers Models for Administrative purpose.'''

from django.contrib import admin
from bucketlist.models import Bucketlist, BucketlistItem

# Register your models here.
admin.site.register(Bucketlist) 
admin.site.register(BucketlistItem)
