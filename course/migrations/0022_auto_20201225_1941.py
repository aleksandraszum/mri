# Generated by Django 3.1 on 2020-12-25 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_auto_20201225_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]