'''Script used to test bucketlist response and request. '''

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class ApiHeaderAuthorization(APITestCase):

    '''Base class used to Attach header to all request on setup.'''

    fixtures = ['initial_fix']

    def setUp(self):

        #Include an appropriate `Authorization:` header on all requests.
        token = Token.objects.get(user__username='samuel')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class ApiUserBucketlist(ApiHeaderAuthorization):

    def test_user_can_view_bucketlist(self):

        url= reverse_lazy('apibucketlist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_create(self):

        data = {'name': 'my bucketlist'}
        url= reverse_lazy('apibucketlist')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_create_error(self):

        data = {'': ''}
        url= reverse_lazy('apibucketlist')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ApiUserNoBucketlist(APITestCase):

    def setUp(self):

        user = User.objects.create_user('lauren',
            'laurenjobs@gmail.com', '12345')       
        self.client = APIClient()
        self.client.login(username='lauren', password='12345')


    def test_user_has_no_bucketlist(self):

        url= reverse_lazy('apibucketlist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class ApiUserBucketlistView(ApiHeaderAuthorization):

    def test_getbucketlistby_id(self):

        url= reverse_lazy('bucketlistdetail', kwargs={'pk':19})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_updatebucketlistby_id(self):

        data = {'name': 'my updated bucketlist'}
        url= reverse_lazy('bucketlistdetail', kwargs={'pk':19})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)


        wrongdata = {'': ''}
        url= reverse_lazy('bucketlistdetail', kwargs={'pk':19})
        response = self.client.put(url, wrongdata)
        self.assertEqual(response.status_code, 200)

    def test_deletedataby_id(self):

        url= reverse_lazy('bucketlistdetail', kwargs={'pk':19})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)