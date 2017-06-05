# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_questforuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultforusercheckintask',
            name='quest',
            field=models.ForeignKey(default=1, to='app.Quests'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resultforuserchoicestask',
            name='quest',
            field=models.ForeignKey(default=1, to='app.Quests'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resultforuserimagetask',
            name='quest',
            field=models.ForeignKey(default=1, to='app.Quests'),
            preserve_default=False,
        ),
    ]
