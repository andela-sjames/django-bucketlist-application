from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .test_bucketlist import ApiHeaderAuthorization


class ApiUserBucketlistItems(ApiHeaderAuthorization):

    def test_user_can_addbucketlist(self):

        data={'name': 'item', 'done': True }
        url= reverse_lazy('addbucketitem', kwargs={'id':19})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ApiUserItemListDetail(ApiHeaderAuthorization):

    def test_user_can_updatebucketlist(self):

        data={'name': 'updateitem', 'done': True }
        url= reverse_lazy('itemdetail', kwargs={'id':19, 'item_id': 24 })
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_cannot_updatebucketlist(self):

        data={'': '', '': '' }
        url= reverse_lazy('itemdetail', kwargs={'id':19, 'item_id': 24 })
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_can_deletebucketlist(self):

        url= reverse_lazy('itemdetail', kwargs={'id':19, 'item_id': 24 })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




