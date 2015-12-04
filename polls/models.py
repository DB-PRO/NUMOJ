from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Permission
import random

# Create your models here.
class Tag(models.Model):
    tagName = models.CharField(max_length = 60)
    
    def __str__(self):
        return self.tagName

class Problem(models.Model):
    tag = models.ManyToManyField(Tag)
    level = models.IntegerField(default = 3)
    problemName = models.CharField(max_length = 60)
    problemStatement = models.CharField(max_length = 60)
    problemDate = models.DateField(max_length = 1, auto_now = True)
    extraInformation = models.CharField(max_length = 1000)
    timelimit = models.FloatField(default = 1)
    input = models.CharField(max_length = 60, default = "null")
    output = models.CharField(max_length = 60, default = "null")
    
    def __str__(self):
        return self.problemName
    
    
class Submission(models.Model):
    type_status = (
        ('Accepted', 'AC'), ('Time limit exceeded', 'TLE'), ('Wrong answer', 'WA')
    )
    
    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(User)
    status = models.CharField(max_length = 20, choices = type_status)
    submittedDate = models.DateTimeField(default=timezone.now)
    Language = models.CharField(default = "C++", max_length = 20)
    Time = models.FloatField(default = 0.0)
    Memory = models.IntegerField(default = 0)
    code = models.CharField(max_length = 1000, default = "..code..")
    
    def __str__(self):
        return self.problem.problemName + ' ' + self.user.username

    
class News(models.Model):
    title = models.CharField(max_length = 1000)
    time = models.DateTimeField(auto_now = True)
    news = models.CharField(max_length = 10000)
    
    def __str__(self):
        return self.news
