'''Script used to test authentication of API views.'''

from rest_framework.test import APIClient
from django.core.urlresolvers import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class ApiUserCreateAccount(APITestCase):

    '''Class defined to test user account creation.'''

    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')

    def test_user_can_signup(self):
        form_data={'username':'andela','password':'andela','email':'andela@andela.com',}
        url=reverse_lazy('register')
        response=self.client.post(url, form_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_get_token(self):
        data={'username':'johndoe', 'password':'12345'}
        url=reverse_lazy('gettoken')
        response=self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        response=self.client.login(username='johndoe', password='12345')
        self.assertEqual(response, True)