"""This module contains views used by the filesharing app."""

import string

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from .file_storage import FileStorage
from .forms import FileUploadForm, NewUserForm
from .models import FileMetadata


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
            file_obj = request.FILES['the_file']
            FileUploadView.save_and_store(request, file_obj)
        except ValueError as err:
            messages.error(request, str(err))
        else:
            messages.success(request, 'File uploaded.')

        return HttpResponseRedirect(reverse('filesharing:index'))

    @staticmethod
    def save_and_store(request, file_obj):
        """Try to save a new file into the system.

        Checks if the given parameter is a valid, new file.
        If this check fails, it raises an error with a human-readable reason.

        If the function succeeds, the file will be uploaded to the file-storage
        service and its metadata will be saved in our local database.
        """
        metadata = FileMetadata.from_file(file_obj, request.user)
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
        metadata.save()


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


@login_required
def index(request):
    """Shows the index page of the website."""
    context = {
        'files': filter(
            lambda metadata: metadata.visible(request.user),
            FileMetadata.objects.all(),
        ),
        'user': request.user,
    }
    return render(request, 'filesharing/index.html', context)
