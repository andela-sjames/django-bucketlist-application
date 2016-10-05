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

    def resolve_all_bucketlist(self, args, context, info):
        # context will reference to the Django request.
        if not context.user.is_authenticated():
            return Bucketlist.objects.none()
        else:
            return Bucketlist.objects.filter(user=context.user)

    def resolve_all_bucketlistitem(self, args, context, info):
        # context will reference to the Django request.
        if not context.user.is_authenticated():
            return BucketlistItem.objects.none()
        else:
            bucketlist = Bucketlist.objects.filter(
            user_id=context.user.id)
            return BucketlistItem.objects.filter(bucketlist=bucketlist)

    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(
    query=Query,
    # mutation=Mutation,
    middlewares=[DjangoDebugMiddleware()],
)
