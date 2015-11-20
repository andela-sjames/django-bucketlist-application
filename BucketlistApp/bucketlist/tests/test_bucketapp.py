from django.test import TestCase, Client, LiveServerTestCase, RequestFactory

from django.core.urlresolvers import resolve, reverse, reverse_lazy
from django.contrib.auth.models import User
from bucketlist.views import CreateBucketlistView, BucketlistView
from django.contrib.messages.storage.fallback import FallbackStorage



class UserCreateViewTestCase(TestCase):

    fixtures = ['initial_fixtures']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.client.login(email='samuel.james@andela.com',
                                 password='samuel')
        self.user= User.objects.get(id=1)




    def test_user_create_edit_view(self):

        data = {'name': 'my bucketlist', 'itemname': 'my item1', 'done': ''}
        data1={'name': 'my new bucketlist'}

        #test user can create bucketlist
        request = self.factory.post('/bucketlist/action/samuel',data1)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = CreateBucketlistView.as_view()(request)


        self.assertEquals(response.status_code, 302)

        #test user can edit bucketlist created
        response = self.client.post(reverse_lazy('deleteupdatebucket', kwargs={
            'id': 19
            }), data1 )
        self.assertEquals(response.status_code, 302)
    


    def test_user_addedit_item(self):

        data={'itemname': 'item2', 'done': 'true' }
        data1={'itemname': 'newitem2', 'done': 'true' }
        emptydata={'itemname': '', 'done': '' }
        #test user can add bucketlist item
        response = self.client.post(reverse_lazy('additem', kwargs={
            'id': 1 }), data )
        self.assertEquals(response.status_code, 302)

        #test user should not submit empty add form
        response = self.client.post(reverse_lazy('additem', kwargs={
            'id': 1
            }), emptydata )
        self.assertEquals(response.status_code, 302)

        #test user can edit bucketlistitem
        response = self.client.post(reverse_lazy('delupdateitem', kwargs={
            'id': 19,
            'item_id': 33 }), data )
        self.assertEquals(response.status_code, 302)

        #test user can delete item created
        response = self.client.get(reverse_lazy('delupdateitem', kwargs={
            'id': 19,
            'item_id': 33
            }), data )
        self.assertEquals(response.status_code, 302)


class UserViewDetailTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')
        self.client.login(email='johndoe@gmail.com',
                                 password='12345')

        

    #user creates a bucketlist

    def test_user_view_detail(self):

        # user can view bucketlist detail
        request =self.factory.get(reverse_lazy('mylist', kwargs={
                    'username':'johndoe'
                    }))
        request.user = self.user
        response = BucketlistView.as_view()(request)

        self.assertEquals(response.status_code, 200)

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
                    }))
        self.assertEquals(response.status_code, 302)

        response =self.client.get(reverse_lazy('mylist', kwargs={
                    'username':'samuel' 
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