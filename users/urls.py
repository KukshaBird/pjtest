from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='user_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='user_detail'),
]