# Generated by Django 3.2 on 2021-04-23 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filesharing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filemetadata',
            old_name='storage_id',
            new_name='storage_path',
        ),
    ]
