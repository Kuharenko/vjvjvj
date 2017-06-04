# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170604_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quests',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_type',
            field=models.CharField(default=b'2', max_length=1, choices=[(b'0', b'\xd0\x9e\xd1\x82\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd1\x8c \xd1\x84\xd0\xbe\xd1\x82\xd0\xbe'), (b'1', b'Check In'), (b'2', b'\xd0\x92\xd1\x8b\xd0\xb1\xd0\xbe\xd1\x80 \xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd0\xb3\xd0\xbe \xd0\xb2\xd0\xb0\xd1\x80\xd0\xb8\xd0\xb0\xd0\xbd\xd1\x82\xd0\xb0')]),
        ),
    ]
