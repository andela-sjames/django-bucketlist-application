from django.conf.urls import url, include
from bucketlist.views import HomePageView, SignInView, SignUpView, DashboardView, SignOutView, BucketItemsView, BucketlistView,ViewBucketlistdetail, AddItemsView, DeleteUpdateBucketlistView,delUpdateItemView


urlpatterns = [
    url(r'^signin/$', SignInView.as_view(), name='signin'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signout/$', SignOutView.as_view(), name='signout'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^(?P<id>[0-9]+)/items/(?P<item_id>[0-9]+)$', delUpdateItemView.as_view(), name='delupdateitem'),
    url(r'^action/(?P<username>\w+)/(?P<id>[0-9]+)$', BucketItemsView.as_view(), name = 'action'),
    url(r'^(?P<username>\w+)/(?P<id>[0-9]+)$', BucketlistView.as_view(), name = 'mylist'),
    url(r'^view/(?P<id>[0-9]+)/items/$', ViewBucketlistdetail.as_view(), name='view'), 
    url(r'^(?P<id>[0-9]+)/items/$', AddItemsView.as_view(), name='additem'), 
    url(r'^(?P<id>[0-9]+)/$', DeleteUpdateBucketlistView.as_view(), name='deleteupdatebucket'),
]