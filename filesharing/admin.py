from django.contrib import admin

from .models import Tag, FileMetadata


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_count')

    def file_count(self, obj):
        return str(FileMetadata.objects.filter(tags__in=[obj.id]).count())
    file_count.short_description = 'Files'


class FileMetadataAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'size', 'owner', 'shown_tags',
        'shown_groups', 'id', 'storage_path'
    )

    def shown_tags(self, obj):
        return ', '.join(map(str, obj.tags.all()))
    shown_tags.short_description = 'Tags'

    def shown_groups(self, obj):
        return str(obj.groups)
    shown_groups.short_description = 'Groups'


admin.site.register(Tag, TagAdmin)
admin.site.register(FileMetadata, FileMetadataAdmin)
