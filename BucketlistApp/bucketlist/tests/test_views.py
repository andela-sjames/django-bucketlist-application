from django.test import TestCase, Client, LiveServerTestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User

class UserSignInViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')

        def test_view_post_auth_signin(self):
        
            data = {'username': 'johndoe@gmail.com', 'password': '12345'}
            response = self.client.post('/', data)
            self.assertEquals(response.status_code, 302)
