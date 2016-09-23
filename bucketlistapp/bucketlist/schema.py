from graphene import relay, ObjectType
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from .models import Bucketlist, BucketlistItem


class BucketlistNode(DjangoNode):
    class Meta:
        model = Bucketlist
        filter_fields = {
            'name': ['icontains', 'istartswith', 'exact'],
            'user': ['exact'],
        }
        filter_order_by = ['name']


class BucketlistItemNode(DjangoNode):
    class Meta:
        model = BucketlistItem
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'bucketlist': ['exact'],
            'bucketlist__name': ['exact'],
        }
        filter_order_by = ['name', 'bucketlist__name']
