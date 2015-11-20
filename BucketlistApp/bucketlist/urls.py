from django.conf.urls import url, include
from bucketlist import views 


urlpatterns = [
    url(r'^(?P<id>[0-9]+)/$', views.DeleteUpdateBucketlistView.as_view(), name='deleteupdatebucket'),
    url(r'^search/(?P<id>[0-9]+)/$', views.SearchListView.as_view(), name='search'),
    url(r'^signin/$', views.SignInView.as_view(), name='signin'),
    url(r'^signout/$', views.SignOutView.as_view(), name='signout'),
    url(r'^(?P<id>[0-9]+)/items/(?P<item_id>[0-9]+)$', views.DelUpdateItemView.as_view(), name='delupdateitem'),

    url(r'^itemdone/(?P<id>[0-9]+)/items/(?P<item_id>[0-9]+)/$', views.ItemDone.as_view(), name='done'),

    url(r'^action/(?P<username>\w+)$', views.CreateBucketlistView.as_view(), name = 'action'),
    url(r'^(?P<username>\w+)/$', views.BucketlistView.as_view(), name = 'mylist'),
    url(r'^view/(?P<id>[0-9]+)/$', views.ViewBucketlistdetail.as_view(), name='view'), 
    url(r'^(?P<id>[0-9]+)/items/$', views.AddItemsView.as_view(), name='additem'), 
]