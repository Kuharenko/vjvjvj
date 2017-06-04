# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quests',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AddField(
            model_name='quests',
            name='picture',
            field=models.ImageField(default=b'', upload_to=b''),
        ),
        migrations.AddField(
            model_name='quests',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AddField(
            model_name='tasks',
            name='location',
            field=models.CharField(default='slug', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasks',
            name='picture',
            field=models.ImageField(default='123', upload_to=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasks',
            name='task_category',
            field=models.ManyToManyField(to='app.TaskCategory'),
        ),
        migrations.RemoveField(
            model_name='tasks',
            name='task_type',
        ),
        migrations.AddField(
            model_name='tasks',
            name='task_type',
            field=models.CharField(default='123', max_length=1, choices=[(b'0', b'\xd0\x9e\xd1\x82\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd1\x8c \xd1\x84\xd0\xbe\xd1\x82\xd0\xbe'), (b'1', b'Check In'), (b'2', b'\xd0\x92\xd1\x8b\xd0\xb1\xd0\xbe\xd1\x80 \xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd0\xb3\xd0\xbe \xd0\xb2\xd0\xb0\xd1\x80\xd0\xb8\xd0\xb0\xd0\xbd\xd1\x82\xd0\xb0')]),
            preserve_default=False,
        ),
    ]
