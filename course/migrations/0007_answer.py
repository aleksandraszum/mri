# Generated by Django 3.1 on 2020-10-14 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=300)),
                ('is_true', models.BooleanField(default=False)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.question')),
            ],
        ),
    ]
