from django.conf.urls import url, include, patterns
from rest_framework.urlpatterns import format_suffix_patterns
from bucketlistapi import views



urlpatterns = [
    url(r'^bucketlists/$', views.BucketList.as_view(),name ='apibucketlist'),
    url(r'^user/register/$', views.create_auth, name='register',),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', views.BucketListDetail.as_view(), name='bucketlistdetail'),
    url(r'^bucketlists/(?P<id>[0-9]+)/items/$', views.AddBucketItem.as_view(), name='addbucketitem'),
    url(r'^bucketlists/(?P<id>[0-9]+)/items/(?P<item_id>[0-9]+)$', views.ItemListDetail.as_view(), name='itemdetail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)