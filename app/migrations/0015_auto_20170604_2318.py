# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20170604_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quests',
            name='tasks_checkin',
            field=models.ManyToManyField(to='app.TaskCheckIn', blank=True),
        ),
        migrations.AlterField(
            model_name='quests',
            name='tasks_choice',
            field=models.ManyToManyField(to='app.TaskChoiceRightVariant', blank=True),
        ),
        migrations.AlterField(
            model_name='quests',
            name='tasks_image',
            field=models.ManyToManyField(to='app.TaskUploadImage', blank=True),
        ),
    ]
