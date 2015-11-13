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
# Create your views here.

for user in User.objects.all():
    Token.objects.get_or_create(user=user)

#for user request for token
def token_request(request):
    if user_requested_token() and token_request_is_warranted():
        new_token = Token.objects.create(user=request.user)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_auth(request, format=None):
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


class BucketList(APIView):
    """
    List all bucketlist, or create a new bucketlist.
    """
    def get(self, request, format=None):
        userid=request.user.id
        bucketlists = Bucketlist.objects.filter(user=userid)
        serializer = BucketlistSerializer(bucketlists, many=True)
        if not serializer.data:
            content={
            'response':'No bucketlist to display'
            }
            return Response(content)
        return Response(serializer.data)

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


class BucketListDetail(APIView):
    """
    Retrieve, update or delete a Bucketlist instance.
    """
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

class AddBucketItem(APIView):

    ''' Create a new bucketlist Item.'''

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



class ItemListDetail(APIView):

    ''' Delete and Update bucketlist items by id.'''
    
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
        #bucketserializer=BucketlistSerializer(bucketlist)
        if itemserializer.is_valid():
            itemserializer.save()
            return Response(itemserializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id, item_id, format=None):

        item=self.check_itemexist(item_id=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        
    


