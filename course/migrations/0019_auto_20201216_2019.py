# Generated by Django 3.1 on 2020-12-16 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0018_auto_20201025_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birth_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='study',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]