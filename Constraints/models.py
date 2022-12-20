from django.db import models


CONSTRAINT_TYPES = (
    ('executing_agency_limit', 'executive agency limit'), 
    ('location_limit', 'location limit'), 
    ('yearly_funding', 'yearly funding')
)


class Constraints(models.Model):
    code = models.CharField(max_length=20)
    max_limit = models.IntegerField()
    constraint_type = models.CharField(max_length=50, choices=CONSTRAINT_TYPES, null=False, blank=False)

    def __str__(self):
        return str(self.code) + "-" + str(self.max_limit) + "-" + str(self.constraint_type)

    class Meta:
        verbose_name_plural = "Constraints"
