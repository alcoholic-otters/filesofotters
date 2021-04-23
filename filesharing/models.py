"""This module contains models for the filesharing app."""

from django.db import models

from .file_storage import FileStorage


# The number of seconds before a download url expires.
URL_EXPIRE = 2 * 60


class FileMetadata(models.Model):
    """The metadata we store locally about a file."""

    name = models.CharField(max_length=128)
    size = models.IntegerField()
    storage_path = models.CharField(max_length=2048)

    def __str__(self):
        return self.name

    @classmethod
    def from_file(cls, file_obj):
        """Derive the `FileMetadata` corresponding to a given file."""
        storage_path = f'uploads/{file_obj.name}'

        return cls(
            name=file_obj.name,
            size=file_obj.size,
            storage_path=storage_path,
        )

    def human_size(self):
        """Return a human-readable string representation of the file size."""
        size = float(self.size)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size < 1000.0:
                break
            size /= 1000.0
        return f'{round(size, 1)} {unit}'

    def download_url(self):
        """Return a URL which can be accessed to download the file."""
        # We need to set content disposition to make sure we download the file,
        # instead of opening it.
        return FileStorage().url(
            name=self.storage_path,
            expire=URL_EXPIRE,
            parameters={
                'ResponseContentDisposition':
                    f'attachment; filename="{self.name}"',
            }
        )
