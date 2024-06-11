from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Create your models here.


class Nutriment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    grams = models.FloatField()
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name}: {self.grams}g, {self.calories}g"


