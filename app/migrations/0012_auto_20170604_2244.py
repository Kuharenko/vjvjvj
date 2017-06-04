# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20170604_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quests',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'static/media/images', blank=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'static/media/images', blank=True),
        ),
    ]
