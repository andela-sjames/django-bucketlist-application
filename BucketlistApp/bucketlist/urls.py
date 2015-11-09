from django.conf.urls import url, include
from bucketlist import views 


urlpatterns = [
    url(r'^search/(?P<id>[0-9]+)$', views.SearchListView.as_view(), name='search'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^signout/$', views.SignOutView.as_view(), name='signout'),
    url(r'^(?P<id>[0-9]+)/items/(?P<item_id>[0-9]+)$', views.delUpdateItemView.as_view(), name='delupdateitem'),
    url(r'^action/(?P<username>\w+)/(?P<id>[0-9]+)$', views.BucketItemsView.as_view(), name = 'action'),
    url(r'^(?P<username>\w+)/(?P<id>[0-9]+)$', views.BucketlistView.as_view(), name = 'mylist'),
    url(r'^view/(?P<id>[0-9]+)/items/$', views.ViewBucketlistdetail.as_view(), name='view'), 
    url(r'^(?P<id>[0-9]+)/items/$', views.AddItemsView.as_view(), name='additem'), 
    url(r'^(?P<id>[0-9]+)/$', views.DeleteUpdateBucketlistView.as_view(), name='deleteupdatebucket'),
]