from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^podstawy_nmr/([0-9]+)/$', views.basic_NMR, name='basicNMR'),
    url(r'^spin_echo/([0-9]+)/$', views.spin_echo, name='spin_echo'),

]
