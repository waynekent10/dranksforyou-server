from django.db import models
from .liquor import Liquor
from .beverage import Beverage

class LiquorBeverage(models.Model):
    liquor = models.ForeignKey(Liquor, on_delete=models.CASCADE)
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE)