''' API view used for response and request. '''

from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from bucketlist.models import Bucketlist, BucketlistItem
from bucketlistapi.serializers import BucketlistSerializer, UserSerializer, BucketlistItemSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .setpagination import LimitOffsetpage

from rest_framework import filters
from rest_framework.generics import GenericAPIView, ListAPIView


class UserRegistration(GenericAPIView):
    serializer_class=UserSerializer

    '''Endpoint for User REgistration.'''
    
    def post(self, request, *args, **kwargs):

        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            content = {
            'status': 'User successfully created, login to continue',
            'username':serialized.data['username'],
            'email': serialized.data['email']
                }
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

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
        create_value=request.data

        userdetail={unicode('user'):unicode(userid),
           unicode('created_by'):unicode(username)}
        create_value.update(userdetail)
        serializer = BucketlistSerializer(data=create_value)

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
        update_bucketist_value=request.data

        userdetail={unicode('user'):unicode(userid),
        unicode('created_by'):unicode(username)}
        update_bucketist_value.update(userdetail)

        serializer = BucketlistSerializer(bucketlist, data=update_bucketist_value)
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

    serializer_class = BucketlistItemSerializer
    pagination_class = LimitOffsetpage

    def check_bucketlistexist(self, id):
        try:
            return Bucketlist.objects.get(id=id)
        except Bucketlist.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):

        bucketlist=self.check_bucketlistexist(id)

        bucketlist_value=request.data
        keyid={unicode('bucketlist'):unicode(id)}
        bucketlist_value.update(keyid)

        itemserializer=BucketlistItemSerializer(data=bucketlist_value)
        bucketserializer=BucketlistSerializer(bucketlist)
        if itemserializer.is_valid():
            itemserializer.save()
            return Response(bucketserializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemListDetail(GenericAPIView):

    ''' Delete and Update bucketlist items by id.'''

    serializer_class = BucketlistItemSerializer
    pagination_class = LimitOffsetpage

    def check_bucketlistexist(self, id):
        try:
            return Bucketlist.objects.get(id=id)
        except Bucketlist.DoesNotExist:
            raise Http404

    def check_itemexist(self, item_id):
        try:
            return BucketlistItem.objects.get(id=item_id)
        except BucketlistItem.DoesNotExist:
            raise Http404

    def put(self, request, id, item_id, format=None):

        bucketlist=self.check_bucketlistexist(id=id)
        item=self.check_itemexist(item_id=item_id)

        update_item_value=request.data
        keyid={unicode('bucketlist'):unicode(id)}
        update_item_value.update(keyid)

        itemserializer = BucketlistItemSerializer(item, data=update_item_value)
        if itemserializer.is_valid():
            itemserializer.save()
            return Response(itemserializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, item_id, format=None):

        item=self.check_itemexist(item_id=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


