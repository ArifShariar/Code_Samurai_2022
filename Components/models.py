from django.db import models


COMPONENT_TYPE = (('goods', 'goods'), ('works', 'works'))


class Components(models.Model):
    component_id = models.CharField(max_length=20)
    project_id = models.CharField(max_length=20)
    executing_agency = models.CharField(max_length=20)
    component_type = models.CharField(max_length=20)
    depends_on = models.CharField(max_length=20, null=True)
    budget_ratio = models.FloatField()

    def __str__(self):
        return self.component_id

