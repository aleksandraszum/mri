# Generated by Django 3.1 on 2020-10-19 15:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_useranswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='result',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
