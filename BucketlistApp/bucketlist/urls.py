from django.conf.urls import url, include
from bucketlist.views import HomePageView, SignInView, SignUpView, DashboardView, SignOutView, BucketItemsView


urlpatterns = [
    url(r'^signin/$', SignInView.as_view(), name='signin'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signout/$', SignOutView.as_view(), name='signout'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
     url(r'^action/(?P<username>\w+)$', BucketItemsView.as_view(), name = 'action'),

]