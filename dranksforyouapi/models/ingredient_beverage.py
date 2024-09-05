from django.db import models
from .ingredient import Ingredient
from .beverage import Beverage

class IngredientBeverage(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE)