from django.contrib import admin

from .models import FileMetadata

class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'storage_id')


admin.site.register(FileMetadata, FileMetadataAdmin)
