from email.policy import default
from enum import unique
from django.db import models


class App(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    image = models.CharField(max_length=200, blank=False)
    command = models.CharField(max_length=200, blank=False)
    envs = models.JSONField()
