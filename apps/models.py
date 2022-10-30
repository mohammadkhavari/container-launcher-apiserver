from django.db import models


class App(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    image = models.CharField(max_length=200, blank=False)
    command = models.CharField(max_length=200, blank=False)
    envs = models.JSONField()

class Run(models.Model):
    created = models.DateTimeField(blank=False)
    containerId = models.CharField(max_length=100, blank=False, primary_key=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=100, blank=False)
    image = models.CharField(max_length=200, blank=False)
    command = models.CharField(max_length=200, blank=False)
    envs = models.JSONField()
