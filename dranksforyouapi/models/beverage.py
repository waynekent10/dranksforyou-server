from django.db import models


class Beverage(models.Model):
    beverage_name = models.CharField(max_length=55)
    liquor_id = models.CharFieldField()
    ingredient = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
