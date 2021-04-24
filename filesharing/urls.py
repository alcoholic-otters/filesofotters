from django.urls import path

from . import views

app_name = 'filesharing'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.FileUploadView.as_view(), name='upload'),
    path('delete/<int:metadata_id>', views.FileDeleteView.as_view(), name='delete'),
]
