from django.db import models
from .beverage import Beverage

class Ingredients(models.Model):
    name = models.CharField(max_length=100)
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE, related_name='ingredients')