# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170604_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='quests',
            name='quest_description',
            field=models.CharField(default=123, max_length=10000),
            preserve_default=False,
        ),
    ]
