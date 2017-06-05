# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0017_resultforusercheckintask_resultforuserchoicestask_resultforuserimagetask'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultQuestByUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_complete', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('status', models.CharField(max_length=b'1', choices=[(b'0', b'IN PROCESS'), (b'1', b'COMPLETED')])),
                ('quest', models.ForeignKey(to='app.Quests')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
