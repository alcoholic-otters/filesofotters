"""This modules contains forms used by the filesharing app."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Tag


class FileUploadForm(forms.Form):
    """The form used to upload a file."""

    the_file = forms.FileField()
    tags = forms.ModelMultipleChoiceField(Tag.objects.all(), required=False)


# We do not use `UserCreationForm` directly, in case we'll want to customize it.
class NewUserForm(UserCreationForm):
    """The form used to register a new user account."""


class GroupCreateForm(forms.Form):
    """The form used to create a new group."""

    name = forms.CharField(max_length=128)

    def clean_name(self):
        # Characters not allowed in group names for certain reasons.
        FORBIDDEN = '<>$"\' \t'

        name = self.cleaned_data['name']
        if any(ch in name for ch in FORBIDDEN):
            raise ValidationError('Group name contains invalid characters.')
        return name


class TagCreateForm(forms.ModelForm):
    """The form used to create a new tag."""

    class Meta:
        model = Tag
        fields = ('name',)

    def clean_name(self):
        # Characters not allowed in tag names for certain reasons.
        FORBIDDEN = '<>$"\' \t'

        name = self.cleaned_data['name']
        if any(ch in name for ch in FORBIDDEN):
            raise ValidationError('Tag name contains invalid characters.')
        return name
