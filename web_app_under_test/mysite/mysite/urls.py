from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^app/', include('app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login, {'template_name': 'app/login.html'}, name='login'),
]
