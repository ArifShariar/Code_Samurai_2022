from django.contrib.auth.models import User
from django.db import models

# Create your models here.


user_types = (('SYSADMIN', 'system admin'), ('ECNEC', 'Executive Committee of National Economic Council'),
              ('MOP', 'Ministry of Planning'), ('EXEC', 'Executing Agency'), ('APP', 'Application Users'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50, choices=user_types, null=True, blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
