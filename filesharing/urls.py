from django.urls import path

from . import views

app_name = 'filesharing'
urlpatterns = [
    path('', views.index, name='index'),
]
