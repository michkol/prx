from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<strona>[0-9]*)$', views.index, name='index'),
    url(r'^kraj/(?P<kraj>[a-z]{2})/(?P<strona>[0-9]*)$', views.index, name='kraj'),
]
