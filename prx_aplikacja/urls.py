from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<strona>[0-9]*)$', views.index, name='index'),
    url(r'^kraj/(?P<kraj>[a-z]{2})/(?P<strona>[0-9]*)$', views.index, name='kraj'),
    url(r'^kraj/$', views.lista_krajow, name='lista_krajow'),
    url(r'^ip/(?P<ip>.*)$', views.index, name='ip'),
    url(r'^losowy$', views.losowy, name='losowy'),
]
