from django.db import models
from django.core.validators import MinValueValidator

from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    color = models.CharField(default='#ff69b4', max_length=7)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Record(models.Model):
    title = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    description = models.TextField(default="")
    value = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    
    is_income = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)