from django.db import models
from .beverage import Beverage

class Liquor(models.Model):
    name = models.ForeignKey(Beverage, on_delete=models.CASCADE)