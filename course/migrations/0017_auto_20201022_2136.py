# Generated by Django 3.1 on 2020-10-22 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0016_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]
