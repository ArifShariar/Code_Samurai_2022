from django.db import models


class Agencies(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.name