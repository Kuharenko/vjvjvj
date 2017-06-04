# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170604_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quests',
            name='tasks',
        ),
        migrations.AddField(
            model_name='quests',
            name='tasks',
            field=models.ManyToManyField(to='app.Tasks'),
        ),
    ]
