from django.db import models

from Code_Samurai_2022 import settings


# Create your models here.


class Project(models.Model):
    project_id = models.CharField(max_length=255)
    exec_by = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    cost = models.FloatField()
    timespan = models.IntegerField()
    goal = models.TextField(max_length=255, null=True)
    start_date = models.DateField()
    completion = models.FloatField()
    actual_cost = models.FloatField()
    is_proposal = models.BooleanField(default=False)
    proposal_date = models.DateField(null=True)

    def __str__(self):
        return self.name
