from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^podstawy_nmr/([0-9]+)/$', views.basic_nmr, name='basicNMR'),
    url(r'^spin_echo/([0-9]+)/$', views.spin_echo, name='spin_echo'),
    url(r'^dane_w_przestrzeni_k/([0-9]+)/$', views.k_space, name='k_space'),
    url(r'^rekonstrukcja_danych/([0-9]+)/$', views.reconstruction, name='reconstruction'),
    url(r'^obrazowanie_dyfuzji/([0-9]+)/$', views.diffusion, name='diffusion'),

]
