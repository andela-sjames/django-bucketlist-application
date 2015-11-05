from django.conf.urls import patterns, include, url
from django.contrib import admin
import bucketlist
import bucketlistapi

urlpatterns = [
  
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bucketlist/', include('bucketlist.urls')),
    url(r'^$', bucketlist.views.HomePageView.as_view(), name='homepage'),
    #url(r'^', include('bucketlistapi.urls')) 
]
