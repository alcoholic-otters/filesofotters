from django.contrib import admin

from .models import Tag, FileMetadata


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'owner', 'shown_tags', 'id', 'storage_path')

    def shown_tags(self, obj):
        return ', '.join(map(str, obj.tags.all()))
    shown_tags.short_description = 'Tags'


admin.site.register(Tag, TagAdmin)
admin.site.register(FileMetadata, FileMetadataAdmin)
