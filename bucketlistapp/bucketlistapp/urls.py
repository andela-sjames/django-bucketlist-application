from django.conf.urls import include, url
from django.contrib import admin
import bucketlist

from bucketlist.schema import schema

from django.views.decorators.csrf import csrf_exempt
from graphene.contrib.django.views import GraphQLView

urlpatterns = [

    url(r'^myappadmin/', include(admin.site.urls)),
    url(r'^bucketlist/', include('bucketlist.urls')),
    url(r'^$', bucketlist.views.SignUpView.as_view(), name='signup'),
    url(r'^api/', include('bucketlistapi.urls')),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(schema=schema))),
    url(r'^graphiql', include('django_graphiql.urls')),

]

urlpatterns += [
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

handler404 = 'bucketlist.views.custom_404'
handler500 = 'bucketlist.views.custom_500'
