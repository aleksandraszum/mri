from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^zaloz_konto/$', views.signup, name='signup'),
    url(r'^wylogowanie/$', views.logout_view, name='logout_view'),
    url(r'^logowanie/$', views.login_view, name='login_view'),
    url(r'^podstawy_nmr/$', views.basic_nmr_base, name='basicNMR_base'),
    url(r'^podstawy_nmr/([0-5])/$', views.basic_nmr, name='basicNMR'),
    url(r'^podstawy_nmr/quiz/$', views.basic_nmr_quiz, name='basicNMR_quiz'),
    url(r'^spin_echo/$', views.spin_echo_base, name='spin_echo_base'),
    url(r'^spin_echo/([0-9])/$', views.spin_echo, name='spin_echo'),
    url(r'^spin_echo/quiz/$', views.spin_echo_quiz, name='spin_echo_quiz'),
    url(r'^dane_w_przestrzeni_k/$', views.k_space_base, name='k_space_base'),
    url(r'^dane_w_przestrzeni_k/([0-9]+)/$', views.k_space, name='k_space'),
    url(r'^dane_w_przestrzeni_k/quiz$', views.k_space_quiz, name='k_space_quiz'),
    url(r'^rekonstrukcja_danych/$', views.reconstruction_base, name='reconstruction_base'),
    url(r'^rekonstrukcja_danych/([0-9]+)/$', views.reconstruction, name='reconstruction'),
    url(r'^obrazowanie_dyfuzji/$', views.diffusion_base, name='diffusion_base'),
    url(r'^obrazowanie_dyfuzji/([0-9]+)/$', views.diffusion, name='diffusion'),
    url(r'^lekcje/$', views.lessons, name='lessons'),

]
