# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse

from django.db import models

class User(models.Model):

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    gender = models.CharField(max_length=20, choices=GENDER)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[self.pk])

class Statistic(models.Model):
    user_id = models.ForeignKey(User, related_name='statistic', on_delete=models.CASCADE)
    date = models.DateField()
    page_views = models.IntegerField()
    clicks = models.IntegerField()
