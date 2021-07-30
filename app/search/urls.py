from django.conf.urls import url, include
from . import views
from django.urls import path

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.return_route, name='test'),
    path('form', views.user_input, name='user_input'),
]
