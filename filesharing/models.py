"""This module contains models for the filesharing app."""

from django.db import models
from django.contrib.auth.models import Group, User

from .file_storage import FileStorage


# The number of seconds before a download url expires.
URL_EXPIRE = 2 * 60


class Tag(models.Model):
    """A tag associated with a file, used for searching."""

    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class UserGroup(Group):
    """A group of users, used for setting the visibility of files."""

    # The separator string used to separate the username from the group name.
    # This allows different users to think they have groups with the same name.
    SEPARATOR = '<>'

    class Meta:
        proxy = True

    @classmethod
    def internal_name(_cls, user, name):
        """The real group name used in the database."""
        return f'{user.username}{UserGroup.SEPARATOR}{name}'

    @classmethod
    def of_user(cls, user, name):
        """Creates a new group belonging to a given user."""
        name = cls.internal_name(user, name)
        return cls.objects.create(name=name)

    @property
    def display_name(self):
        """The group name which should be seen by users."""
        return self.name.split(UserGroup.SEPARATOR)[1]

    @property
    def owner_name(self):
        """The name of the group owner."""
        return self.name.split(UserGroup.SEPARATOR)[0]

    @property
    def owner(self):
        """The group owner object."""
        return User.objects.get(username=self.owner_name)


class FileMetadata(models.Model):
    """The metadata we store locally about a file."""

    name = models.CharField(max_length=128)
    size = models.IntegerField()
    storage_path = models.CharField(max_length=2048)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    groups = models.ManyToManyField(UserGroup)
    tags = models.ManyToManyField(Tag, 'file_set')

    def __str__(self):
        return self.name

    @classmethod
    def from_file(cls, file_obj, owner):
        """Derive the `FileMetadata` corresponding to a given file."""
        storage_path = f'uploads/{owner.username}/{file_obj.name}'

        return cls(
            name=file_obj.name,
            size=file_obj.size,
            storage_path=storage_path,
            owner=owner,
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

    def visible(self, user):
        """Check if the file can be accessed by a user."""
        return self.owner == user or any(g in self.groups.all() for g in user.groups.all())
