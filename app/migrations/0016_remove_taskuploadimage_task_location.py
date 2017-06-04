# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20170604_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskuploadimage',
            name='task_location',
        ),
    ]
