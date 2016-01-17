from django.conf.urls import include, url
from django.contrib import admin
import bucketlist

urlpatterns = [

    url(r'^myappadmin/', include(admin.site.urls)),
    url(r'^bucketlist/', include('bucketlist.urls')),
    url(r'^$', bucketlist.views.SignUpView.as_view(), name='signup'),
    url(r'^api/', include('bucketlistapi.urls')),

]

urlpatterns += [
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

handler404 = 'bucketlist.views.custom_404'
handler500 = 'bucketlist.views.custom_500'
