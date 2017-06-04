# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170604_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quests',
            name='tasks',
            field=models.ManyToManyField(related_name='tsk', to='app.Tasks'),
        ),
    ]
