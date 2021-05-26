"""This module contains unit tests for the filesharing app."""

from django.contrib.auth.models import User
from django.test import TestCase

from .models import FileMetadata, UserGroup

class FileAccessTestCase(TestCase):
    """Test cases related to file access."""

    def setUp(self):
        self.owner = User.objects.create_user(username='bula')
        self.stranger = User.objects.create_user(username='stranger')
        self.friend = User.objects.create_user(username='friend')

        self.group = UserGroup.of_user(self.owner, 'for_friends')
        self.group.save() # Save to get an ID.
        self.group.user_set.add(self.friend)
        self.group.save()

        self.metadata = FileMetadata.objects.create(
            name='tempfile', size=1, owner=self.owner
        )
        self.metadata.groups.set([self.group])

    def test_owner_can_view_their_file(self):
        """Owners can view files that belong to them."""
        self.assertTrue(self.metadata.visible(self.owner))

    def test_strangers_cannot_view_files(self):
        """Complete strangers cannot view files they don't own."""
        self.assertFalse(self.metadata.visible(self.stranger))

    def test_group_members_can_view_files(self):
        """
        Users who don't own a file can still view it if in the right groups.
        """
        self.assertTrue(self.metadata.visible(self.friend))
