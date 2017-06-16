# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0021_imagetaskmoderate'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagetaskmoderate',
            name='task',
            field=models.ForeignKey(default=1, to='app.TaskUploadImage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagetaskmoderate',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagetaskmoderate',
            name='user_answer',
            field=models.ImageField(null=True, upload_to=b'static/media/images', blank=True),
        ),
        migrations.AlterField(
            model_name='imagetaskmoderate',
            name='quest',
            field=models.ForeignKey(to='app.Quests'),
        ),
    ]
