"""This module contains code for storing user files externally."""

from storages.backends.s3boto3 import S3Boto3Storage


class FileStorage(S3Boto3Storage):
    """A storage class used to interact with user-submitted files."""

    bucket_name = 'filesofotters'
