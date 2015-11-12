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


class UserCreateViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')
        self.client.login(email='johndoe@gmail.com',
                                 password='12345')


    def test_user_create_edit_view(self):

        data = {'name': 'my bucketlist', 'itemname': 'my item1', 'done': ''}
        data1={'name': 'my new bucketlist'}

        #test user can create bucketlist
        response =self.client.post(reverse_lazy('action', kwargs={
                'username':'johndoe' ,
                'id':1
                }), data )
        self.assertEquals(response.status_code, 302)

        #test user can edit bucketlist created
        response = self.client.post(reverse_lazy('deleteupdatebucket', kwargs={
            'id': 1
            }), data1 )
        self.assertEquals(response.status_code, 302)

        #test user can delete bucketlist created
        response = self.client.get(reverse_lazy('deleteupdatebucket', kwargs={
            'id': 1
            }), data1 )
        self.assertEquals(response.status_code, 302)
        


    def test_user_addedit_item(self):

        data={'itemname': 'item2', 'done': 'true' }
        data1={'itemname': 'newitem2', 'done': 'true' }
        emptydata={'itemname': '', 'done': '' }
        #test user can add bucketlist item
        response = self.client.post(reverse_lazy('additem', kwargs={
            'id': 1
            }), data )
        self.assertEquals(response.status_code, 302)

        #test user should not submit empty add form
        response = self.client.post(reverse_lazy('additem', kwargs={
            'id': 1
            }), emptydata )
        self.assertEquals(response.status_code, 302)

        #test user can edit bucketlistitem
        response = self.client.post(reverse_lazy('delupdateitem', kwargs={
            'id': 1,
            'item_id': 1
            }), data )
        self.assertEquals(response.status_code, 302)

        #test user can delete item created
        response = self.client.get(reverse_lazy('delupdateitem', kwargs={
            'id': 1,
            'item_id': 1
            }), data )
        self.assertEquals(response.status_code, 302)


class UserViewDetailTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')
        self.client.login(email='johndoe@gmail.com',
                                 password='12345')

    #user creates a bucketlist

    def test_user_view_detail(self):

        data = {'name': 'my bucketlist', 'itemname': 'my item1', 'done': ''}
        response =self.client.post(reverse_lazy('action', kwargs={
                    'username':'johndoe' ,
                    'id':1
                    }), data )
        self.assertEquals(response.status_code, 302)

        # user can view bucketlist detail
        response =self.client.get(reverse_lazy('mylist', kwargs={
                    'username':'johndoe' ,
                    'id':1
                    }))
        self.assertEquals(response.status_code, 302)

        #user can view bucketlist and items detail
        response =self.client.get(reverse_lazy('view', kwargs={
                    'id':1
                    }))
        self.assertEquals(response.status_code, 200)


class UserViewpaginationTestCase(TestCase):

    fixtures = ['initial_fixtures']

    def setUp(self):
        self.client = Client()

        self.client.login(email='samuel.james.@andela.com',
                                 password='samuel')


    def test_user_view_paginated(self):
        # user can view bucketlist detail
        response =self.client.get('/bucketlist/samuel/1&page=2')
        self.assertEquals(response.status_code, 200)

        #user calls first page
        response =self.client.get('/bucketlist/samuel/1&page=1')
        self.assertEquals(response.status_code, 200)

        # user can view bucketlist detail
        response =self.client.get(reverse_lazy('mylist', kwargs={
                    'username':'samuel' ,
                    'id':1
                    }))
        self.assertEquals(response.status_code, 302)

        response =self.client.get(reverse_lazy('mylist', kwargs={
                    'username':'samuel' ,
                    'id':1
                    }))
        self.assertEquals(response.status_code, 302)


    def test_search_list(self):

        response =self.client.get(reverse_lazy('search', kwargs={
                    'id':1
                    }), data={'q': 'name'})
        self.assertEquals(response.status_code, 200)



    def test_wrong_user_login(self):

        response =self.client.login(email='johndoe@gmail.com',
                                 password='12345')

        self.assertEquals(response, False)





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










