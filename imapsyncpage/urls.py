from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^$', views.index, name='index'),
            url('transfer', views.get_form, name='get_form '),
            #url('test', views.test, name='test '),
            url('hello', views.hello, name='hello '),
            url('home', views.home, name='home '),
#            url('masstransfer', views.masstransfer, name='masstransfer '),
            ]
