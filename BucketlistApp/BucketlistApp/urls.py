from django.conf.urls import patterns, include, url
from rest_framework.authtoken import views
from django.contrib import admin
import bucketlist
import bucketlistapi

urlpatterns = [
  
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bucketlist/', include('bucketlist.urls')),
    url(r'^$', bucketlist.views.HomePageView.as_view(), name='homepage'),
    url(r'^api/', include('bucketlistapi.urls')),
   
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
     url(r'^api/auth/login/', views.obtain_auth_token)
]
