"""This module contains models for the filesharing app."""

from django.db import models


class FileMetadata(models.Model):
    """The metadata we store locally about a file."""

    name = models.CharField(max_length=128)
    size = models.IntegerField()
    storage_id = models.CharField(max_length=2048)

    def __str__(self):
        return self.name

    @classmethod
    def from_file(cls, file_obj):
        """Derive the `FileMetadata` corresponding to a given file."""
        storage_id = f'uploads/{file_obj.name}'

        return cls(
            name=file_obj.name,
            size=file_obj.size,
            storage_id=storage_id,
        )
