# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170604_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quests',
            name='tasks',
        ),
        migrations.AddField(
            model_name='quests',
            name='tasks',
            field=models.ForeignKey(default=132, to='app.Tasks'),
            preserve_default=False,
        ),
    ]
