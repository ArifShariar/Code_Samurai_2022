from django.db import models


COMPONENT_TYPE = (('goods', 'goods'), ('works', 'works'))


class Components(models.Model):
    component_id = models.CharField(max_length=20, null=False)
    project_id = models.CharField(max_length=20, null=False)
    executive_agency = models.CharField(max_length=20, null=False)
    component_type = models.CharField(max_length=20, null=False)
    depends_on = models.CharField(max_length=20)
    budget_ratio = models.FloatField()

    def __str__(self):
        return self.component_id

