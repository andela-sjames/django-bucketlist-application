from django.test import TestCase, Client, LiveServerTestCase
from django.core.urlresolvers import resolve, reverse, reverse_lazy
from django.contrib.auth.models import User

class UserAuthViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')

    def test_view_homepage(self):
        """Test that user request for homepage binds to a view class called `SignUpView`.
        """

        response = resolve('/')
        self.assertEquals(response.func.__name__, 'SignUpView')

    def test_user_post_signin(self):
        """Test that user post to signin route has a session
        """
        data = {'email': 'johndoe@gmail.com', 'password': '12345'}
        response = self.client.post('/bucketlist/signin/', data)
        self.assertEquals(response.status_code, 302)

    def test_user_signout(self):

        response = self.client.get(reverse_lazy('signout'))
        self.assertEquals(response.status_code, 302)

    def test_view_non_user_Signin(self):
        
        data = {'email': 'joh@gmail.com', 'password': '12345'}
        response = self.client.post('/bucketlist/signin/', data)
        self.assertEquals(response.status_code, 302)

    def test_view_wrong_password_Signin(self):
        
        data = {'email': 'johndoe@gmail.com', 'password': '123454444'}
        response = self.client.post('/bucketlist/signin/', data)
        self.assertEquals(response.status_code, 302)



class UserRegistrationViewTest(TestCase):

    fixtures = ['initial_fixtures']
    '''
    Test class to user registration.
    '''
    def setUp(self):
        '''
        User sign's up with data.
        '''
        self.client_stub = Client()

        self.form_data = dict(
            username="andela",
            password1="andela",
            password2="andela",
            email="andela@andela.com",
        )
        self.form_data2 = dict(
            username="",
            password1="",
            password2="and",
            email="andela.com",
        )

    def test_view_reg_route(self):

        data=dict(
            username="andela",
            password1="andela",
            password2="andela",
            email="samuel.james@andela.com",
        )
        '''
        User is redirected after signup data is validated.
        '''
        response = self.client_stub.post('/', self.form_data)
        self.assertEquals(response.status_code, 302)

        #user told email already taken
        response = self.client_stub.post('/', data)
        self.assertEquals(response.status_code, 200)

        #user told password not strong
        response = self.client_stub.post('/', self.form_data2)
        self.assertEquals(response.status_code, 200)

        #signup or homepage is called
        response = self.client_stub.get('/')
        self.assertEquals(response.status_code, 200)