# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from recipe_management import settings


class Recipe(models.Model):
    """Basic Recipe model class"""
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    stepwise_directions = models.CharField(max_length=1000)
    ingredients = models.CharField(max_length=1000)
    picture = models.ImageField(default=None)
