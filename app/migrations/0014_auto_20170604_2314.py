# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20170604_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='task_category',
        ),
        migrations.DeleteModel(
            name='Tasks',
        ),
    ]
