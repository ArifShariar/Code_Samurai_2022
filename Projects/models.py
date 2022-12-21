from django.db import models

from Users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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
    start_date = models.DateField(null=True)
    completion = models.FloatField(null=True)
    actual_cost = models.FloatField(null=True)
    is_proposal = models.BooleanField(default=False)
    proposal_date = models.DateField(null=True)
    created_by = models.ForeignKey(User, related_name='UserFK', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    project = models.ForeignKey(Project, related_name='projectFK', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1, null=True)
    feedback = models.TextField(max_length=500)
    created_by = models.ForeignKey(User, related_name='UserFKey', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.feedback
