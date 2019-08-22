# coding = utf-8

from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^send_email$', views.send_email, name='send_email'),
    url(r'^login$', views.login, name='login'),

]
