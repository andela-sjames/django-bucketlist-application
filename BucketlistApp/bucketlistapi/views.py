''' API view used for response and request. '''

from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from bucketlist.models import Bucketlist, BucketlistItems
from bucketlistapi.serializers import BucketlistSerializer, UserSerializer, BucketlistItemsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .setpage import LimitOffsetpage


from rest_framework import filters
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
# Create your views here.

class UserRegistration(CreateAPIView):

    '''Endpoint for User REgistration.'''

    serializer_class=UserSerializer

class BucketList(ListAPIView):

    """
    List all bucketlist, or create a new bucketlist.
    """
    model = Bucketlist
    serializer_class = BucketlistSerializer
    pagination_class = LimitOffsetpage
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')

    def get_queryset(self):
        """
        This view should return a list of all the bucketlist
        for the currently authenticated user.
        """
        
        quser=self.request.user.id
        queryset = Bucketlist.objects.filter(user=quser)
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(name__icontains=q)

        return queryset

    def post(self, request, format=None):

        userid=request.user.id
        username=request.user.username
        val=request.data

        userdetail={unicode('user'):unicode(userid),
           unicode('created_by'):unicode(username)}
        val.update(userdetail)
        serializer = BucketlistSerializer(data=val)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BucketListDetail(GenericAPIView):
    """
    Retrieve, update or delete a Bucketlist instance.
    """
    model = Bucketlist
    serializer_class = BucketlistSerializer
    pagination_class = LimitOffsetpage

    def get_object(self, pk):
        try:
            return Bucketlist.objects.get(pk=pk)
        except Bucketlist.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bucketlist = self.get_object(pk)
        serializer = BucketlistSerializer(bucketlist)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        bucketlist = self.get_object(pk)

        userid=request.user.id
        username=request.user.username
        val=request.data

        userdetail={unicode('user'):unicode(userid),
        unicode('created_by'):unicode(username)}
        val.update(userdetail)

        serializer = BucketlistSerializer(bucketlist, data=val)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        bucketlist = self.get_object(pk)
    
        bucketlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddBucketItem(GenericAPIView):

    ''' Create a new bucketlist Item.'''

    serializer_class = BucketlistItemsSerializer
    pagination_class = LimitOffsetpage

    def check_bucketlistexist(self, id):
        try:
            return Bucketlist.objects.get(id=id)
        except Bucketlist.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):

        bucketlist=self.check_bucketlistexist(id)

        val=request.data
        keyid={unicode('bucketlist'):unicode(id)}
        val.update(keyid)

        itemserializer=BucketlistItemsSerializer(data=val)
        bucketserializer=BucketlistSerializer(bucketlist)
        if itemserializer.is_valid():
            itemserializer.save()
            return Response(bucketserializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ItemListDetail(GenericAPIView):

    ''' Delete and Update bucketlist items by id.'''

    serializer_class = BucketlistItemsSerializer
    pagination_class = LimitOffsetpage

    def check_bucketlistexist(self, id):
        try:
            return Bucketlist.objects.get(id=id)
        except Bucketlist.DoesNotExist:
            raise Http404

    def check_itemexist(self, item_id):
        try:
            return BucketlistItems.objects.get(id=item_id)
        except BucketlistItems.DoesNotExist:
            raise Http404


    def put(self, request, id, item_id, format=None):

        bucketlist=self.check_bucketlistexist(id=id)
        item=self.check_itemexist(item_id=item_id)

        input_value=request.data
        keyid={unicode('bucketlist'):unicode(id)}
        input_value.update(keyid)

        itemserializer = BucketlistItemsSerializer(item, data=input_value)
        if itemserializer.is_valid():
            itemserializer.save()
            return Response(itemserializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id, item_id, format=None):

        item=self.check_itemexist(item_id=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


