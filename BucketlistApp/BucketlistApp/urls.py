from django.conf.urls import patterns, include, url
from rest_framework.authtoken import views
from django.contrib import admin
from django.conf import settings
import bucketlist
import bucketlistapi

urlpatterns = [
  
    url(r'^myappadmin/', include(admin.site.urls)),
    url(r'^bucketlist/', include('bucketlist.urls')),
    url(r'^$', bucketlist.views.SignUpView.as_view(), name='signup'),
    url(r'^api/', include('bucketlistapi.urls')),
   
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
     url(r'^api/auth/login/', views.obtain_auth_token)
]

handler404='bucketlist.views.custom_404'
handler500='bucketlist.views.custom_500'

#test command.
#coverage run --source bucketlist/ manage.py test bucketlist

