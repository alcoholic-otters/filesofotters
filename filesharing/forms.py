"""This modules contains forms used by the filesharing app."""

from django import forms


class FileUploadForm(forms.Form):
    """The form used to upload a file."""

    the_file = forms.FileField()
