from django.db import models
from googleapiclient.model import Model

# Create your models here.
class UserLogs(models.Model):
    user = models.CharField(max_length=30)
    login_time = models.DateField()
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.user