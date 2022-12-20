from django.db import models

# Create your models here.


class Constraints(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    max_projects = models.IntegerField()

    def __str__(self):
        return str(self.latitude) + "-" + str(self.longitude) + "-" + str(self.max_projects)

    class Meta:
        verbose_name_plural = "Constraints"
