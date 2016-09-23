import graphene
from graphene import relay, ObjectType
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from graphene.contrib.django.debug import DjangoDebugMiddleware, DjangoDebug

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


class Query(ObjectType):

    bucketlist = relay.NodeField(BucketlistNode)
    all_bucketlist = DjangoFilterConnectionField(BucketlistNode)

    Bucketlistitem = relay.NodeField(BucketlistItemNode)
    all_bucketlistitem = DjangoFilterConnectionField(BucketlistItemNode)

    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(
    query=Query,
    # mutation=Mutation,
    middlewares=[DjangoDebugMiddleware()],
)
