# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


class TaskCategory(models.Model):
    category_name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.category_name


class TaskChoiceRightVariant(models.Model):
    task_name = models.CharField(max_length=80)
    task_description = models.CharField(max_length=100)
    task_question = models.CharField(max_length=100)
    task_variant1 = models.CharField(max_length=50)
    task_variant2 = models.CharField(max_length=50)
    task_variant3 = models.CharField(max_length=50)
    task_variant4 = models.CharField(max_length=50)
    task_variant_right = models.CharField(max_length=50)
    task_type = models.CharField(max_length=1, default='2')
    task_category = models.ManyToManyField(TaskCategory)
    picture = models.ImageField(upload_to='static/media/images', null=True, blank=True)

    def __unicode__(self):
        return self.task_name


class TaskCheckIn(models.Model):
    task_name = models.CharField(max_length=80)
    task_description = models.CharField(max_length=100)
    task_question = models.CharField(max_length=100)
    task_location = models.CharField(max_length=100)
    task_type = models.CharField(max_length=1, default='1')
    task_category = models.ManyToManyField(TaskCategory)
    picture = models.ImageField(upload_to='static/media/images', null=True, blank=True)

    def __unicode__(self):
        return self.task_name


class TaskUploadImage(models.Model):
    task_name = models.CharField(max_length=80)
    task_description = models.CharField(max_length=100)
    task_question = models.CharField(max_length=100)
    task_type = models.CharField(max_length=1, default='0')
    user_image = models.ImageField(upload_to='static/media/images', null=True, blank=True)
    task_category = models.ManyToManyField(TaskCategory)
    picture = models.ImageField(upload_to='static/media/images', null=True, blank=True)

    def __unicode__(self):
        return self.task_name


class Quests(models.Model):
    quest_name = models.CharField(max_length=100)
    quest_description = models.CharField(max_length=10000)
    tasks_choice = models.ManyToManyField(TaskChoiceRightVariant, blank=True)
    tasks_checkin = models.ManyToManyField(TaskCheckIn, blank=True)
    tasks_image = models.ManyToManyField(TaskUploadImage, blank=True)
    picture = models.ImageField(upload_to='static/media/images', null=True, blank=True)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return self.quest_name


class ResultForUserImageTask(models.Model):
    STATUS = (
        ('0','IN PROCESS'),
        ('1','COMPLETED'),
    )
    task_id = models.ForeignKey(TaskUploadImage)
    user = models.ForeignKey(User)
    quest = models.ForeignKey(Quests)
    user_answer = models.ImageField(upload_to='static/media/images', null=True, blank=True)
    date_complete = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length='1', choices=STATUS)

    def __unicode__(self):
        return str(self.id)


class ResultForUserChoicesTask(models.Model):
    STATUS = (
        ('0','IN PROCESS'),
        ('1','COMPLETED'),
    )
    task_id = models.ForeignKey(TaskChoiceRightVariant)
    user = models.ForeignKey(User)
    quest = models.ForeignKey(Quests)
    user_answer = models.CharField(max_length=100)
    date_complete = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length='1', choices=STATUS)

    def __unicode__(self):
        return str(self.id)


class ResultForUserCheckinTask(models.Model):
    STATUS = (
        ('0','IN PROCESS'),
        ('1','COMPLETED'),
    )
    task_id = models.ForeignKey(TaskCheckIn)
    quest = models.ForeignKey(Quests)
    user = models.ForeignKey(User)
    user_answer = models.CharField(max_length=100)
    date_complete = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length='1', choices=STATUS)

    def __unicode__(self):
        return str(self.id)


class ResultQuestByUser(models.Model):
    STATUS = (
        ('0', 'IN PROCESS'),
        ('1', 'COMPLETED'),
    )
    quest = models.ForeignKey(Quests)
    user = models.ForeignKey(User)
    date_complete = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length='1', choices=STATUS)

    def __unicode__(self):
        return str(self.id)


class QuestForUser(models.Model):
    user = models.ForeignKey(User)
    quest = models.ManyToManyField(Quests, blank=True)

    def __unicode__(self):
        return str(self.id)