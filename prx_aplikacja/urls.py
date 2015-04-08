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
]
