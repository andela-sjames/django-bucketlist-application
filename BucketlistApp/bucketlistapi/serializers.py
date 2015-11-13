from rest_framework import serializers
from bucketlist.models import BucketlistItems, Bucketlist
from django.contrib.auth.models import User

class BucketlistItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model=BucketlistItems
        fields=('id', 'name', 'date_created', 'date_modified', 'done', 'bucketlist')


class BucketlistSerializer(serializers.ModelSerializer):

    items= BucketlistItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Bucketlist
        fields = ('id','name','items','date_created', 'date_modified', 'created_by', 'user') 
        

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields= ('username','email','password')

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

