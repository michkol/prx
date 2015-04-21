from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<strona>[0-9]*)$', views.lista, name='lista'),

    # przekierowanie dawniej używanych skrótów nazw krajów
    url(r'^kraj/(?P<skrot>gb|tp|zr)/(?P<dalsza_sciezka>.*)$', views.stary_kraj, name='stary_kraj'),

    url(r'^kraj/(?P<kraj>[a-z]{2})/(?P<strona>[0-9]*)$', views.lista, name='kraj'),
    url(r'^kraj/$', views.lista_krajow, name='lista_krajow'),
    url(r'^ip/(?P<ip>.*)$', views.lista, name='ip'),
    url(r'^losowy$', views.losowy, name='losowy'),
    url(r'^dodaj$', views.dodaj, name='dodaj'),
    
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^admin/logowanie$', views.admin_logowanie, name='admin_logowanie'),
    url(r'^admin/pinger$', views.admin_pinger, name='admin_pinger'),
    url(r'^admin/sprawdz_ip$', views.admin_sprawdz_ip, name='admin_sprawdz_ip'),
    url(r'^admin/dodaj$', views.admin_dodaj, name='admin_dodaj'),
]
