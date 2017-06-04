# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
# Create your models here.


class TaskCategory(models.Model):
    category_name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.category_name


class Tasks(models.Model):
    TASK_TYPE = (
        ('0', 'Отправить фото'),
        ('1', 'Check In'),
        ('2', 'Выбор привильного варианта'),
    )
    task_name = models.CharField(max_length=80)
    task_description = models.CharField(max_length=100)
    task_type = models.CharField(max_length=1, choices=TASK_TYPE, default='2')
    task_category = models.ManyToManyField(TaskCategory)
    picture = models.ImageField(upload_to='images',null=True, blank=True)
    location = models.CharField(max_length=100)

    def __unicode__(self):
        return self.task_name


class Quests(models.Model):
    quest_name = models.CharField(max_length=100)
    quest_description = models.CharField(max_length=10000)
    tasks = models.ManyToManyField(Tasks)
    picture = models.ImageField(upload_to='images', null=True, blank=True)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return self.quest_name

