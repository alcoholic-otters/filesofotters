from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('filesharing/', include('filesharing.urls')),
    path('admin/', admin.site.urls),
]
