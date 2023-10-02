from django.db import models

# Create your models here.
class Setting(models.Model):
    name = models.CharField(max_length=20, unique=True)
    value = models.CharField(max_length=100, default='')

    def __str__(self) -> str:
        return '{0} = {1}'.format(self.name, self.value)