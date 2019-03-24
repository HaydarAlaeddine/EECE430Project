from django.urls import path
from . import views
from .views import login_root, login_success, login_fail

from django.conf.urls import url
urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login/$', login_root, name='login_root'),
    url(r'^login/success/$', login_success, name='login_success'),
    url(r'^login/fail/$', login_fail, name='login_fail')

]