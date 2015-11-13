from django.contrib import admin
from bucketlist.models import Bucketlist, BucketlistItems 

# Register your models here.

admin.site.register(Bucketlist)
admin.site.register(BucketlistItems)
