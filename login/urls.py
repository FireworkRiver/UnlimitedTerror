from django.conf.urls import url
from login.views import *

app_name = 'login'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^logout/$', logout, name='logout'),
]
