from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^$', views.index, name='index'),
            url('redre', views.get_form, name='get_form '),
            ]
