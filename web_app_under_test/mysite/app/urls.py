from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact-form$', views.ContactView.as_view(), name='contact-form'),
    url(r'^thanks$', views.thanks, name='thanks'),
]
