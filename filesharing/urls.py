from django.urls import path

from . import views

app_name = 'filesharing'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.FileUploadView.as_view(), name='upload'),
    path('delete/<int:metadata_id>', views.FileDeleteView.as_view(), name='delete'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('tag/create/', views.TagCreateView.as_view(), name='tag-create'),
    path('tag/delete/<int:id>/', views.TagDeleteView.as_view(), name='tag-delete'),
    path('search/', views.FileSearchView.as_view(), name='search'),
]
