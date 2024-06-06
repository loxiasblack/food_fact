from django.db import models

# Create your models here.
class FoodItem(models.Model):
    name = models.CharField("food name", max_length=100)
    calories = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    carbohydrates = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    
    
