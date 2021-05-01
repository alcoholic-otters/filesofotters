from django.contrib import admin

from .models import FileMetadata

class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'id', 'storage_path')


admin.site.register(FileMetadata, FileMetadataAdmin)
