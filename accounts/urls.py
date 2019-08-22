# coding = utf-8

from django.conf.urls import url
from accounts import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^send_email$', views.send_email, name='send_email'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
]
