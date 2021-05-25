"""This module contains views used by the filesharing app."""

import string

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from .file_storage import FileStorage
from .forms import FileGroupSetForm, FileUploadForm, GroupCreateForm, NewUserForm, TagCreateForm
from .models import FileMetadata, Tag, UserGroup


# The maximum size, in bytes, allowed for uploaded files.
MAX_ALLOWED_FILE_SIZE = 5242880 # 5 MB

# The maximum number of characters allowed in a filename.
MAX_FILENAME_LENGTH = 128

# The list of characters which can be used in filenames.
FILENAME_CHARS = string.ascii_letters + string.digits + '-_.'


class FileUploadView(LoginRequiredMixin, View):
    """A view used to upload a file to the system."""

    def post(self, request, *_args, **_kwargs):
        form = FileUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'Form is invalid.')
            return HttpResponseRedirect(reverse('filesharing:index'))

        try:
            user = request.user
            file_obj = request.FILES['the_file']
            tags = form.cleaned_data.get('tags', [])
            FileUploadView.save_and_store(user, file_obj, tags)
        except ValueError as err:
            messages.error(request, str(err))
        else:
            messages.success(request, 'File uploaded.')

        return HttpResponseRedirect(reverse('filesharing:index'))

    @staticmethod
    def save_and_store(user, file_obj, tags):
        """Try to save a new file into the system.

        Checks if the given parameter is a valid, new file.
        If this check fails, it raises an error with a human-readable reason.

        If the function succeeds, the file will be uploaded to the file-storage
        service and its metadata will be saved in our local database.
        """
        metadata = FileMetadata.from_file(file_obj, user)
        storage = FileStorage()

        if file_obj.size > MAX_ALLOWED_FILE_SIZE:
            raise ValueError('File is too large.')

        if len(metadata.name) > MAX_FILENAME_LENGTH:
            raise ValueError('Filename is too long.')

        if any(ch not in FILENAME_CHARS for ch in metadata.name):
            raise ValueError('Filename contains forbbiden characters.')

        if storage.exists(metadata.storage_path):
            raise ValueError('File already exists.')

        storage.save(metadata.storage_path, file_obj)

        metadata.save()         # Save metadata to get an ID.
        metadata.tags.set(tags)
        metadata.save()         # Save with tags.


class FileDeleteView(LoginRequiredMixin, View):
    """A view used to download a file from the system."""

    def dispatch(self, request, *args, **kwargs):
        # Because HTML forms do not handle DELETE requests, we POST a form
        # from the frontend, and submit an extra parameter to specify the
        # HTTP method we really want.
        # https://stackoverflow.com/questions/36455189/put-and-delete-django
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(request, *args, **kwargs)

        return super(FileDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, metadata_id, *_args, **_kwargs):
        metadata = get_object_or_404(FileMetadata, pk=metadata_id)
        storage = FileStorage()

        storage.delete(metadata.storage_path) # Delete from external storage.
        metadata.delete()                     # Delete local metadata.

        messages.success(request, 'File deleted successfully.')
        return HttpResponseRedirect(reverse('filesharing:index'))


class RegisterView(View):
    """A view used to register new user accounts."""

    def get(self, request, *_args, **_kwargs):
        return render(request, 'filesharing/register.html', {})

    def post(self, request, *_args, **_kwargs):
        form = NewUserForm(request.POST)
        if not form.is_valid():
            for (field, reasons) in form.errors.items():
                for reason in reasons:
                    messages.error(request, field + ': ' + reason)
            return HttpResponseRedirect(reverse('filesharing:register'))

        form.save()

        messages.success(request, 'Registration successful')
        return HttpResponseRedirect(reverse('filesharing:register'))


class LoginView(View):
    """A view used to log into an account."""

    def get(self, request, *_args, **_kwargs):
        return render(request, 'filesharing/login.html', {})

    def post(self, request, *_args, **_kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials.')
            return HttpResponseRedirect(reverse('filesharing:login'))

        login(request, user)

        return HttpResponseRedirect(reverse('filesharing:index'))


class LogoutView(View):
    """A view used to log a user out."""

    def post(self, request, *_args, **_kwargs):
        logout(request)

        return HttpResponseRedirect(reverse('filesharing:login'))


class ManageGroupsView(LoginRequiredMixin, View):
    """A view used to manage a user's groups."""

    def get(self, request, *_args, **_kwargs):
        visible = lambda group: group.owner == request.user

        context = {
            'groups': list(filter(visible, UserGroup.objects.all())),
        }
        return render(request, 'filesharing/groups.html', context)


class GroupCreateView(LoginRequiredMixin, View):
    """A view used to create a new group."""

    def post(self, request, *_args, **_kwargs):
        form = GroupCreateForm(request.POST)
        if not form.is_valid():
            for reasons in form.errors.values():
                for reason in reasons:
                    messages.error(request, reason)
            return HttpResponseRedirect(reverse('filesharing:manage-groups'))

        try:
            group = UserGroup.of_user(request.user, form.cleaned_data['name'])
            group.save()
            messages.success(request, 'Group created successfully.')
        except Exception as err:
            messages.error(request, err)

        return HttpResponseRedirect(reverse('filesharing:manage-groups'))


class GroupDeleteView(LoginRequiredMixin, View):
    """A view used to delete an existing group."""

    def get(self, request, *_args, **kwargs):
        group = UserGroup.objects.get(id=kwargs.get('id'))
        if group and group.owner == request.user:
            group.delete()
            messages.success(request, 'Group deleted successfully.')

        return HttpResponseRedirect(reverse('filesharing:manage-groups'))


class GroupMemberAddView(LoginRequiredMixin, View):
    """A view used to add a new member to a group."""

    def post(self, request, *_args, **_kwargs):
        group_id = request.POST['group_id']
        username = request.POST['username']

        try:
            GroupMemberAddView.add_to_group(request.user, group_id, username)
            messages.success(request, 'Member added.')
        except ValueError as err:
            messages.error(request, err)

        return HttpResponseRedirect(reverse('filesharing:manage-groups'))

    @staticmethod
    def add_to_group(user, group_id, username):
        """Add a user to a group.

        If the operation fails, it raises an error with a human-readable reason.
        """
        group = UserGroup.objects.filter(pk=group_id).first()
        if not group:
            raise ValueError('Group does not exist.')
        if group.owner != user:
            raise ValueError('You are not the owner of the group.')

        member = User.objects.filter(username=username).first()
        if not member:
            raise ValueError('No such user.')
        if member == user:
            raise ValueError('You cannot add yourself to a group.')

        group.user_set.add(member)
        group.save()


class GroupMemberRemoveView(LoginRequiredMixin, View):
    """A view used to remove a user from a group."""

    def get(self, request, *_args, **kwargs):
        id = kwargs.get('id')
        username = kwargs.get('username')

        try:
            GroupMemberRemoveView.remove_from_group(request.user, id, username)
            messages.success(request, 'Removed user from group.')
        except ValueError as err:
            messages.error(request, err)

        return HttpResponseRedirect(reverse('filesharing:manage-groups'))

    @staticmethod
    def remove_from_group(user, group_id, username):
        """Remove a user from a group.

        If the operation fails, it raises an error with a human-readable reason.
        """
        group = UserGroup.objects.filter(pk=group_id).first()
        if not group:
            raise ValueError('Group does not exist.')
        if group.owner != user:
            raise ValueError('You are not the owner of the group.')

        member = User.objects.filter(username=username).first()
        if not member:
            raise ValueError('No such user.')

        group.user_set.remove(member)
        group.save()


class TagCreateView(LoginRequiredMixin, View):
    """A view used to create a new tag."""

    def post(self, request, *_args, **_kwargs):
        form = TagCreateForm(request.POST)
        if not form.is_valid():
            for reasons in form.errors.values():
                for reason in reasons:
                    messages.error(request, reason)
            return HttpResponseRedirect(reverse('filesharing:index'))

        form.save()

        messages.success(request, 'New tag created.')
        return HttpResponseRedirect(reverse('filesharing:index'))


class TagDeleteView(LoginRequiredMixin, View):
    """A view used to delete an existing tag."""

    def get(self, _request, *_args, **kwargs):
        tag = Tag.objects.get(id=kwargs.get('id'))
        if tag:
            tag.delete()

        return HttpResponseRedirect(reverse('filesharing:index'))


class TagDetachView(LoginRequiredMixin, View):
    """A view used for detaching a tag from a file."""

    def post(self, request, *_args, **kwargs):
        metadata = FileMetadata.objects.get(id=kwargs.get('file_id'))
        tag = Tag.objects.get(id=kwargs.get('tag_id'))
        redirect_url = request.POST.get('next', reverse('filesharing:index'))

        if metadata.owner != request.user:
            messages.error('You are not the owner of this file.')
            return HttpResponseRedirect(redirect_url)

        metadata.tags.remove(tag)
        return HttpResponseRedirect(redirect_url)


class FileSearchView(LoginRequiredMixin, View):
    """A view used for searching files."""

    def post(self, request, *_args, **_kwargs):
        search = request.POST.get('search')
        tag_ids = request.POST.getlist('search_tags')

        return HttpResponseRedirect(
            f'{reverse("filesharing:index")}?search={search}&tags={",".join(tag_ids)}'
        )


class DetailFileView(LoginRequiredMixin, View):
    """A view used to display details about a file."""

    def get(self, request, *_args, **kwargs):
        file = get_object_or_404(FileMetadata, pk=kwargs.get('id'))
        visible_group = lambda group: group.owner == request.user

        if file.owner != request.user:
            messages.error(request, 'You are not the owner of the file.')
            return HttpResponseRedirect(reverse('filesharing:index'))

        context = {
            'file': file,
            'groups': list(filter(visible_group, UserGroup.objects.all())),
        }
        return render(request, 'filesharing/detail_file.html', context)


class FileGroupsSetView(LoginRequiredMixin, View):
    """A view used to expose a file to some group."""

    def post(self, request, *_args, **kwargs):
        file_id = kwargs.get('id')
        form = FileGroupSetForm(request.POST)

        if not form.is_valid():
            messages.error(request, 'Form is invalid.')
            return HttpResponseRedirect(
                reverse('filesharing:detail-file', args=[file_id])
            )

        try:
            groups = form.cleaned_data.get('groups')
            FileGroupsSetView.set_groups(request.user, file_id, groups)
            messages.success(request, 'Groups set.')
        except ValueError as err:
            messages.error(request, err)

        return HttpResponseRedirect(
            reverse('filesharing:detail-file', args=[file_id])
        )

    @staticmethod
    def set_groups(user, file_id, groups):
        """Sets the groups which can view  a file.

        If the operation fails, it raises an error with a human-readable reason.
        """
        metadata = FileMetadata.objects.get(pk=file_id)
        if metadata.owner != user:
            raise ValueError('You are not the owner of the file.')

        metadata.groups.set(groups)
        metadata.save()


@login_required
def index(request):
    """Shows the index page of the website."""
    search = request.GET.get('search', '')
    tag_ids = request.GET.get('tags', '')

    files = FileMetadata.objects.all()

    # Keep only the files the user searched for.
    if search:
        files = files.filter(name__icontains=search)
    if tag_ids:
        tag_ids = list(map(int, tag_ids.split(',')))
        files = files.filter(tags__in=tag_ids).distinct() # Check this.

    # Keep only files the user is allowed to see.
    visible_to_user = lambda metadata: metadata.visible(request.user)
    files = list(filter(visible_to_user, files))

    context = {
        'files': files,
        'user': request.user,
        'request': request,
        'tags': Tag.objects.all(),
        'groups': UserGroup.objects.all(),
    }
    return render(request, 'filesharing/index.html', context)
