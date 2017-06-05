# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0016_remove_taskuploadimage_task_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultForUserCheckinTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_answer', models.CharField(max_length=100)),
                ('date_complete', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('status', models.CharField(max_length=b'1', choices=[(b'0', b'IN PROCESS'), (b'1', b'COMPLETED')])),
                ('task_id', models.ForeignKey(to='app.TaskCheckIn')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResultForUserChoicesTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_answer', models.CharField(max_length=100)),
                ('date_complete', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('status', models.CharField(max_length=b'1', choices=[(b'0', b'IN PROCESS'), (b'1', b'COMPLETED')])),
                ('task_id', models.ForeignKey(to='app.TaskChoiceRightVariant')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResultForUserImageTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_answer', models.ImageField(null=True, upload_to=b'static/media/images', blank=True)),
                ('date_complete', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('status', models.CharField(max_length=b'1', choices=[(b'0', b'IN PROCESS'), (b'1', b'COMPLETED')])),
                ('task_id', models.ForeignKey(to='app.TaskUploadImage')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
