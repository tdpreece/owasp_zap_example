from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', login, {'template_name': 'app/login.html'}, name='login'),
    url(r'^contact-form$', csrf_exempt(login_required(views.ContactView.as_view())), name='contact-form'),
    url(r'^thanks$', views.thanks, name='thanks'),
]
