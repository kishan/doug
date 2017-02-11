from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<address>[a-z]*[0-9]+)/$', views.senators_phone, name='senators_phone'),
    url(r'^test/$', views.webhook, name='webhook'),
