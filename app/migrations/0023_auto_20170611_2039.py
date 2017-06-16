# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20170611_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultforuserimagetask',
            name='status',
            field=models.CharField(max_length=b'1', choices=[(b'0', b'IN PROCESS'), (b'1', b'COMPLETED'), (b'2', b'Moderating')]),
        ),
    ]
