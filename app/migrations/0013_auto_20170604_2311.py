# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170604_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCheckIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_name', models.CharField(max_length=80)),
                ('task_description', models.CharField(max_length=100)),
                ('task_question', models.CharField(max_length=100)),
                ('task_location', models.CharField(max_length=100)),
                ('task_type', models.CharField(default=b'1', max_length=1)),
                ('picture', models.ImageField(null=True, upload_to=b'static/media/images', blank=True)),
                ('task_category', models.ManyToManyField(to='app.TaskCategory')),
            ],
        ),
        migrations.CreateModel(
            name='TaskChoiceRightVariant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_name', models.CharField(max_length=80)),
                ('task_description', models.CharField(max_length=100)),
                ('task_question', models.CharField(max_length=100)),
                ('task_variant1', models.CharField(max_length=50)),
                ('task_variant2', models.CharField(max_length=50)),
                ('task_variant3', models.CharField(max_length=50)),
                ('task_variant4', models.CharField(max_length=50)),
                ('task_variant_right', models.CharField(max_length=50)),
                ('task_type', models.CharField(default=b'2', max_length=1)),
                ('picture', models.ImageField(null=True, upload_to=b'static/media/images', blank=True)),
                ('task_category', models.ManyToManyField(to='app.TaskCategory')),
            ],
        ),
        migrations.CreateModel(
            name='TaskUploadImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_name', models.CharField(max_length=80)),
                ('task_description', models.CharField(max_length=100)),
                ('task_question', models.CharField(max_length=100)),
                ('task_location', models.CharField(max_length=100)),
                ('task_type', models.CharField(default=b'0', max_length=1)),
                ('user_image', models.ImageField(null=True, upload_to=b'static/media/images', blank=True)),
                ('picture', models.ImageField(null=True, upload_to=b'static/media/images', blank=True)),
                ('task_category', models.ManyToManyField(to='app.TaskCategory')),
            ],
        ),
        migrations.RemoveField(
            model_name='quests',
            name='tasks',
        ),
        migrations.AddField(
            model_name='quests',
            name='tasks_checkin',
            field=models.ManyToManyField(to='app.TaskCheckIn'),
        ),
        migrations.AddField(
            model_name='quests',
            name='tasks_choice',
            field=models.ManyToManyField(to='app.TaskChoiceRightVariant'),
        ),
        migrations.AddField(
            model_name='quests',
            name='tasks_image',
            field=models.ManyToManyField(to='app.TaskUploadImage'),
        ),
    ]
