from django.db import models

from Code_Samurai_2022 import settings


# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    exec_by = models.CharField(max_length=255)
    cost = models.FloatField()
    timespan = models.CharField(max_length=255)
    project_id = models.CharField(max_length=255)
    goal = models.CharField(max_length=255)
    start_date = models.DateField()
    completion = models.FloatField()
    actual_cost = models.FloatField()

    def __str__(self):
        return self.name
