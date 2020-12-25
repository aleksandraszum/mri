# Generated by Django 3.1 on 2020-10-14 14:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0013_delete_useranswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('answer_1_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_1', to='course.answer')),
                ('answer_2_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_2', to='course.answer')),
                ('answer_3_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_3', to='course.answer')),
                ('answer_4_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_4', to='course.answer')),
                ('answer_5_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_5', to='course.answer')),
                ('answer_6_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_6', to='course.answer')),
                ('answer_7_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_7', to='course.answer')),
                ('answer_8_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_8', to='course.answer')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.lesson')),
                ('question_1_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_1', to='course.question')),
                ('question_2_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_2', to='course.question')),
                ('question_3_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_3', to='course.question')),
                ('question_4_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_4', to='course.question')),
                ('question_5_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_5', to='course.question')),
                ('question_6_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_6', to='course.question')),
                ('question_7_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_7', to='course.question')),
                ('question_8_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_8', to='course.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]