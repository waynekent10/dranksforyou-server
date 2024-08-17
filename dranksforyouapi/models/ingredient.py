from django.db import models
from .beverage import Beverage

class Ingredients(models.Model):
    name = models.ForeignKey(Beverage, on_delete=models.CASCADE)