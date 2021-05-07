"""This modules contains forms used by the filesharing app."""

from django import forms
from django.contrib.auth.forms import UserCreationForm

class FileUploadForm(forms.Form):
    """The form used to upload a file."""

    the_file = forms.FileField()


# We do not use `UserCreationForm` directly, in case we'll want to customize it.
class NewUserForm(UserCreationForm):
    """The form used to register a new user account."""
