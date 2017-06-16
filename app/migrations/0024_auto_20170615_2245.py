# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20170611_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='modelOne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='modelOneTwo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('model1', models.ForeignKey(to='app.modelOne')),
            ],
        ),
        migrations.CreateModel(
            name='modelTwo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='modelonetwo',
            name='model2',
            field=models.ForeignKey(to='app.modelTwo'),
        ),
    ]
