# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20170606_0143'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageTaskModerate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quest', models.ForeignKey(to='app.ResultForUserImageTask')),
            ],
        ),
    ]
